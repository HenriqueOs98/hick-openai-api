import datetime
import boto3
import os
from urllib.parse import unquote
from src.chat_openai import call_openai
from conversores import criar_documento_txt


s3 = boto3.client('s3')
openai_key = "babuska"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("token_por_documento")
table_tokens_totais = dynamodb.Table("tokens_totais")


def lambda_handler(event, context):
    print(event)
    
    s3_record = event['Records'][0]['s3']
    bucket_name = s3_record['bucket']['name']
    object_key = unquote(s3_record['object']['key'])
    
    print("Object Key:", object_key)
    
    object_content = s3.get_object(Bucket=bucket_name, Key=object_key)['Body'].read().decode('utf-8')
    
    base_name = os.path.basename(object_key)
    file_name, _ = os.path.splitext(base_name)
    
    respostas, payload = call_openai(object_content, openai_key.get_secret_value(), file_name)
    
    doc_txt = criar_documento_txt(respostas)
    salvar_dynamo(table, payload)
    salva_total_tokens(table_tokens_totais, payload)
    now = datetime.datetime.now()

    # Define the S3 object key
    s3_object_key = f"{now.strftime('%Y-%m-%d')}/{file_name}-{now.strftime('%H%M%S')}.txt"

    # Put the object into S3
    s3.put_object(Bucket='sua-generativa-output-bucket', Key=s3_object_key, Body=doc_txt)

def salvar_dynamo(filename, payload):
    now = datetime.datetime.now()
    formatted_date_time = now.isoformat()

    item = {
        "id_documento": filename,
        "data_hora": formatted_date_time,
        "perguntas": payload,
    }

    table.put_item(Item=item)

def salva_total_tokens(new_tokens):
    partitions = []

    for index in new_tokens:
        response = table_tokens_totais.get_item(Key={"modelo": index})
        partitions.append(response)

    result = {}

    # Iterate over the dictionaries in partitions
    for partition in partitions:
        modelo1 = partition.get("Item", {}).get("modelo")
        if modelo1 is None:
            continue

        # Iterate over the dictionaries in new_tokens
        for partition2 in new_tokens:
            modelo2 = partition2.get("modelo")
            if modelo2 is None:
                continue

            # Check if the modelos match
            if modelo1 == modelo2:
                # Sum the values of the other keys
                for key in partition.get("Item", {}):
                    if key == "modelo":
                        continue

                    if key in partition2:
                        result.setdefault(key, 0)
                        result[key] += partition2[key]

    return result