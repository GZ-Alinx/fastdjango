from django.http import JsonResponse
from .aws_access import aws_init
from .aws_ec2 import create_ec2_instance, describe_ec2_instances, start_ec2_instance, stop_ec2_instance, terminate_ec2_instance,get_vpc_info
from .aws_security import create_security_group, describe_security_group, delete_security_group
from .aws_cloudwatch import create_cloudwatch_alarm, delete_cloudwatch_alarm, describe_cloudwatch_alarms
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# 初始化 AWS session
aws_session = aws_init()


# EC2 相关接口
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def aws_create_ec2(request):
    """
    # 请求数据包含以下参数：
    'image_id': 'ami-0613c0d249e70078a',   # Amazon Linux 2023 AMI - ami-0f71013b2c8bd2c29 64/x86 / ami-0613c0d249e70078a 64位/ARM
    {
        "instance_type": "t2.micro", 
        "image_id": "ami-0f71013b2c8bd2c29",
        "volume_size": 300,
        "volume_type": "gp3",
        "iops": 3000,
        "instance_count": 1,
        "security_group_ids": ["sg-0e9390c2429a2bc2f"],
        "key_name": "base-free",
        "subnet_id": "subnet-0e00b7cc263b57bee"
    }

    # doc: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/run_instances.html
    """
    ec2_client = aws_session.client('ec2')
    try:
        response = create_ec2_instance(ec2_client, request.data)
        return JsonResponse({"ec2": response}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def aws_show_ec2(request):
    # 请求数据包含以下参数：
        # 'instance_id': 可选, 实例 ID (例如: "i-1234567890abcdef0")
        # 如果不传 'instance_id'，则返回所有实例信息
    ec2_client = aws_session.client('ec2')
    try:
        response = describe_ec2_instances(ec2_client, request.data.get('instance_id'))
        return JsonResponse({"ec2": response}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def aws_start_ec2(request):
    # 请求数据包含以下参数：
        # 'instance_id': 必须, 要启动的实例 ID (例如: "i-1234567890abcdef0")
    ec2_client = aws_session.client('ec2')
    try:
        response = start_ec2_instance(ec2_client, request.data.get('instance_id'))
        return JsonResponse({"ec2": response}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def aws_stop_ec2(request):
    # 请求数据包含以下参数：
        # 'instance_id': 必须, 要停止的实例 ID (例如: "i-1234567890abcdef0")
    ec2_client = aws_session.client('ec2')
    try:
        response = stop_ec2_instance(ec2_client, request.data.get('instance_id'))
        return JsonResponse({"ec2": response}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def aws_delete_ec2(request):
    # 请求数据包含以下参数：
        # 'instance_id': 必须, 要删除的实例 ID (例如: "i-1234567890abcdef0")
    ec2_client = aws_session.client('ec2')
    try:
        response = terminate_ec2_instance(ec2_client, request.data.get('instance_id'))
        return JsonResponse({"ec2": response}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# 安全组相关接口
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def aws_vpc_info(request):
    # 请求数据包含以下参数：
    # 'group_name': 必须, 安全组名称 (例如: "my-security-group")
    # 'description': 必须, 安全组描述 (例如: "My security group")
    # 'vpc_id': 可选, 关联的 VPC ID (例如: "vpc-12345678")
    try:
        ec2_client = aws_session.client('ec2')
        vpcid = get_vpc_info(ec2_client)
        print("vpc_id", vpcid)
        return JsonResponse({"message": "vpc get success", "data": vpcid}, status=201)
    except Exception as e:
        return JsonResponse({"message": "vpc get failed", "error:": e}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def aws_create_security_group(request):
    # 请求数据包含以下参数：
    # 'group_id': 可选, 要查看的安全组 ID (例如: "sg-12345678")
    # 如果不传 'group_id'，则返回所有安全组的信息
    ec2_client = aws_session.client('ec2')
    vpcid = get_vpc_info(ec2_client)
    print("vpc_id", vpcid)
    
    try:
        response = create_security_group(ec2_client, request.data)
        return JsonResponse({"security_group": response}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def aws_show_security_group(request):
    # 请求数据包含以下参数：
    # 'group_id': 可选, 要查看的安全组 ID (例如: "sg-12345678")
    # 如果不传 'group_id'，则返回所有安全组的信息
    ec2_client = aws_session.client('ec2')
    try:
        response = describe_security_group(ec2_client, request.data.get('group_id'))
        return JsonResponse({"security_group": response}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def aws_delete_security_group(request):
    # 请求数据包含以下参数：
    # 'group_id': 必须, 要删除的安全组 ID (例如: "sg-12345678")
    ec2_client = aws_session.client('ec2')
    try:
        response = delete_security_group(ec2_client, request.data.get('group_id'))
        return JsonResponse({"message": "Security group deleted", "security_group": response}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def aws_edit_security_group(request):
    ec2_client = aws_session.client('ec2')
    try:
        response = delete_security_group(ec2_client, request.data.get('group_id'))
        return JsonResponse({"message": "Security group deleted", "security_group": response}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# CloudWatch 相关接口
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def aws_create_cloudwatch(request):
     # 请求数据包含以下参数：
    # 'alarm_name': 必须, 告警名称 (例如: "my-cloudwatch-alarm")
    # 'metric_name': 必须, 指标名称 (例如: "CPUUtilization")
    # 'namespace': 必须, 告警所属的命名空间 (例如: "AWS/EC2")
    # 'threshold': 必须, 触发告警的阈值 (例如: 80.0)
    # 'comparison_operator': 必须, 比较运算符 (例如: "GreaterThanOrEqualToThreshold")
    cloudwatch_client = aws_session.client('cloudwatch')
    try:
        response = create_cloudwatch_alarm(cloudwatch_client, request.data)
        return JsonResponse({"cloudwatch": response}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def aws_show_cloudwatch(request):
    # 请求数据包含以下参数：
    # 'alarm_name': 可选, 告警名称 (例如: "my-cloudwatch-alarm")
    # 如果不传 'alarm_name'，则返回所有告警的信息
    cloudwatch_client = aws_session.client('cloudwatch')
    try:
        response = describe_cloudwatch_alarms(cloudwatch_client, request.data.get('alarm_name'))
        return JsonResponse({"cloudwatch": response}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def aws_delete_cloudwatch(request):
    # 请求数据包含以下参数：
    # 'alarm_name': 必须, 要删除的告警名称 (例如: "my-cloudwatch-alarm")

    cloudwatch_client = aws_session.client('cloudwatch')
    try:
        response = delete_cloudwatch_alarm(cloudwatch_client, request.data.get('alarm_name'))
        return JsonResponse({"message": "CloudWatch alarm deleted", "cloudwatch": response}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)