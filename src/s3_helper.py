def s3helper():

    s3_record = event['Records'][0]['s3']
    bucket_name = s3_record['bucket']['name']
    object_key = s3_record['object']['key']
    
    object_from_event = s3_client.get_object(Bucket=bucket_name, Key=sobject_key)

    
    object_content = object_from_event['Body'].read().decode('utf-8')

    local_file_path = f"/tmp/{os.path.basename(object_key)}"

        

    try:
        # Upload the file content to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_object_key,
            Body=object_content,
            ContentType='text/plain'  # Specify the content type if necessary
        )

        return {
            'statusCode': 200,
            'body': 'File uploaded to S3 successfully'
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': 'Error uploading file to S3'
        }