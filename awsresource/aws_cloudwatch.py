from .aws_access import *

def create_cloudwatch_alarm(cloudwatch_client, data):
    return cloudwatch_client.put_metric_alarm(
        AlarmName=data.get('alarm_name'),
        MetricName=data.get('metric_name'),
        Namespace=data.get('namespace'),
        Period=data.get('period'),
        EvaluationPeriods=data.get('evaluation_periods'),
        Threshold=data.get('threshold'),
        ComparisonOperator=data.get('comparison_operator'),
        AlarmActions=data.get('alarm_actions')
    )

def delete_cloudwatch_alarm(cloudwatch_client, alarm_name):
    return cloudwatch_client.delete_alarms(AlarmNames=[alarm_name])

def describe_cloudwatch_alarms(cloudwatch_client, alarm_name=None):
    if alarm_name:
        return cloudwatch_client.describe_alarms(AlarmNames=[alarm_name])
    return cloudwatch_client.describe_alarms()
