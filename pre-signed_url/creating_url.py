import boto3
import sys

def presigned_s3_url(bucket, key, expiration):
    
#    Usage:
#        python generatePreSignedUrl.py anS3Bucket Key -e 28800
#        python generatePreSignedUrl.py anS3Bucket Key - default exp= 1 hour 
# key - is the name of file 
    params = {
        'Bucket': bucket,
        'Key': key
    }
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url('get_object', Params=params, ExpiresIn=expiration)
    print(url)

if __name__ == '__main__':
    bucket = str(sys.argv[1])
    key = str(sys.argv[2])
    if len(sys.argv) > 3:
        if str(sys.argv[3]) == "-e":
            expiration = int(sys.argv[4])
    else:
        expiration = 3600
    presigned_s3_url(bucket, key, expiration)
