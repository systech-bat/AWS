import os
import boto3

from flask import Flask, session, redirect, escape, request

# URL 1 hour exp default
def presigned_s3_url(bucket, key, expiration):
    params = {
        'Bucket': bucket,
        'Key': key
    }
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url('get_object', Params=params, ExpiresIn=expiration)
    return(url)

# app_name
app = Flask(__name__)


# secret_key
app.secret_key = os.environ.get('SECRET_KEY', default=None)

@app.route('/')
def index():
    pre_signed_url = presigned_s3_url('pre-signed-url-lab', 'testchart01.png', 3660)
    html_out = '''<!DOCTYPE html> 
                    <html> 
                      <head> 
                        <title>
                           HTML img src Attribute 
                        </title>
                      </head>
                      <body>
                        <h1>Image from pre-signed URL</h1>
                        <img src= {0} alt="Pre-Signed URL generated image link"> 
                      </body>
                      </html>'''.format(pre_signed_url)

    return html_out
