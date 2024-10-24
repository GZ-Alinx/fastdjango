from django.urls import path
from . import views

urlpatterns = [
    path('ec2/create',  views.aws_create_ec2, name='aws_create_ec2'),
    path('ec2/show',  views.aws_show_ec2, name='aws_show_ec2'),
    path('ec2/delete',  views.aws_delete_ec2, name='aws_delete_ec2'),
    path('ec2/start',  views.aws_start_ec2, name='aws_start_ec2'),
    path('ec2/stop',  views.aws_stop_ec2, name='aws_stop_ec2'),
    path('ec2/vpc/show',  views.aws_vpc_info, name='aws_vpc_info'),

    path('sec/create',  views.aws_create_security_group, name='aws_create_security_group'),
    path('sec/edit',  views.aws_edit_security_group, name='aws_edit_security_group'),
    path('sec/delete',  views.aws_delete_security_group, name='aws_delete_security_group'),
    path('sec/show',  views.aws_show_security_group, name='aws_show_security_group'),

    path('cloudwatch/create',  views.aws_create_cloudwatch, name='aws_create_cloudwatch'),
    path('cloudwatch/edit',  views.aws_delete_cloudwatch, name='aws_delete_cloudwatch'),
    path('cloudwatch/delete',  views.aws_delete_cloudwatch, name='aws_delete_cloudwatch'),
    path('cloudwatch/show',  views.aws_show_cloudwatch, name='aws_show_cloudwatch'),
    
    path('cloudwatch/alert/create',  views.aws_show_cloudwatch, name='aws_show_cloudwatch'),
    path('cloudwatch/alert/edit',  views.aws_show_cloudwatch, name='aws_show_cloudwatch'),
    path('cloudwatch/alert/delete',  views.aws_show_cloudwatch, name='aws_show_cloudwatch'),
    path('cloudwatch/alert/show',  views.aws_show_cloudwatch, name='aws_show_cloudwatch'),
]

