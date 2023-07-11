from google.cloud import storage

def upload_img():
    client = storage.Client.from_service_account_json('bill-crawler-88dae2622248.json')
    bucket = client.bucket('bill-bucket-forgm')
    urls = []
    for i in range(0,2):
        blob = bucket.blob('bill-'+str(i)+'.png')
        blob.upload_from_filename('/tmp/page-'+str(i)+'.png')
        urls.append(blob.public_url)
    return urls

# def upload_captcha():
#     client = storage.Client.from_service_account_json('bill-crawler-88dae2622248.json')
#     bucket = client.bucket('bill-bucket-forgm')
#     blob = bucket.blob('herokuCaptcha.png')
#     blob.upload_from_filename('/tmp/captcha.png')
