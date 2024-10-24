from .aws_access import *


# 创建安全组 安全组规则放通80 443 22端口 并处理ip地址（内网/外网）
def create_security_group(ec2_client, vpc_id, group_name, description):
    try:
        response = ec2_client.create_security_group(
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id
        )
        security_group_id = response['GroupId']

        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )
        return security_group_id
    except Exception as e:
        return f"Error: {str(e)}"

def describe_security_group(ec2_client, group_id):
    return ec2_client.describe_security_groups(GroupIds=[group_id])


def delete_security_group(ec2_client, group_id):
    return ec2_client.delete_security_group(GroupId=group_id)
