from .aws_access import *



def get_vpc_info(ec2_client):
    try:
        vpc = ec2_client.describe_vpcs()
        vpcs = vpc.get('Vpcs', [])
        if not vpcs:
            return "No VPCs found."

        vpc_info_list = []
        for vpc in vpcs:
            vpc_id = vpc['VpcId']  # VPC ID
            vpc_name = next((tag['Value'] for tag in vpc.get('Tags', []) if tag['Key'] == 'Name'), "No Name")  # VPC 名称
            state = vpc.get('State', 'Unknown')  # VPC 状态（默认值为 'Unknown'）
            is_default = vpc.get('IsDefault', False)  # 是否为默认 VPC

            vpc_info_list.append({
                "vpc_id": vpc_id,
                "vpc_name": vpc_name,
                "state": state,
                "is_default": is_default
            })

        return vpc_info_list

    except Exception as e:
        return f"Error: {str(e)}"


# 这里创建ec2的时候希望加上安全组 安全组规则放通80 443 22端口 并处理ip地址（内网/外网）
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

def create_ec2_instance(ec2_client, data):
    # 这里可以添加更多的参数来设置实例，例如安全组、键盘等
    return ec2_client.run_instances(
        ImageId=data.get('image_id'),
        InstanceType=data.get('instance_type'),
        # KeyName=data.get('key_name'),
        MinCount=1,
        MaxCount=1,
        SubnetId=data.get('subnet_id'),
        SecurityGroupIds=data.get('security_group_ids'),
    )



# show ec2
def describe_ec2_instances(ec2_client, instance_id=None):
    if instance_id:
        return ec2_client.describe_instances(InstanceIds=[instance_id])
    return ec2_client.describe_instances()


# start ec2
def start_ec2_instance(ec2_client, instance_id):
    return ec2_client.start_instances(InstanceIds=[instance_id])


# stop ec2
def stop_ec2_instance(ec2_client, instance_id):
    return ec2_client.stop_instances(InstanceIds=[instance_id])


# delete ec2
def terminate_ec2_instance(ec2_client, instance_id):
    return ec2_client.terminate_instances(InstanceIds=[instance_id])
