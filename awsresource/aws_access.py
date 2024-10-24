from django.conf import settings
import boto3

# 初始化会话Session
def aws_init():
    AWS_Session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    return AWS_Session
