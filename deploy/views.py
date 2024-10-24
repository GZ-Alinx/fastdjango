import jenkins
from django.http import JsonResponse
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

def jenkins_init():
    """Initialize Jenkins server connection."""
    return jenkins.Jenkins(settings.JENKINS_URL, username=settings.JENKINS_USERNAME, password=settings.JENKINS_PASSWORD)


# 不适用csrf的防护机制， 生产环境中需要改变此策略
# @csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_job(request):
    """
    Create a new job in Jenkins based on the request data.
        {
            "jobname":"Pipeline-02",
            "projectYype": "go",
            "environment":"test",
        "deployhost":"127.0.0.1",
        "code_url":"http://localhost:8080/"
        }
    ---
    responses:
        200:
            description: A successful response
    """
    try:
        request_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

    job_name = request_data.get('jobname')
    project_type = request_data.get('projectYype')
    environment = request_data.get('environment')
    deploy_host = request_data.get('deployhost')
    code_url = request_data.get('code_url')
    if not job_name or not project_type:
        return JsonResponse({"error": "Missing required fields: jobname, projectType"}, status=400)

    server = jenkins_init()
    user = server.get_whoami()

    version = server.get_version()
    print("jenkins: ", user, version)

    # Log the Jenkins user and version (could use logging instead)
    # print(f'Hello {user["fullName"]} from Jenkins {version}')
    if project_type == "php":
        pipeline_config = generate_pipeline_config_php(code_url,environment,deploy_host)
    elif project_type == "java":
        pipeline_config = generate_pipeline_config_java(code_url,environment,deploy_host)
    elif project_type == "cpp":
        pipeline_config = generate_pipeline_config_cpp(code_url,environment,deploy_host)
    elif project_type == "static_web":
        pipeline_config = generate_pipeline_config_static_web(code_url,environment,deploy_host)

    else:
        return JsonResponse({"error": "Invalid project type"}, status=400)

    # Call the generic job creation function
    job_creation_status = create_job_if_not_exists(server, job_name, pipeline_config)

    if job_creation_status:
        return JsonResponse({"message": "Jenkins Pipeline job created successfully!"})
    else:
        return JsonResponse({"error": f"Jenkins job '{job_name}' already exists!"}, status=400)




@csrf_exempt  # 可选：如果需要禁用 CSRF 保护
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_job(request):
    """Run a Jenkins job.

    {
        "jobname":"Pipeline-02"
    }
    """

    try:
        # 从请求中获取作业名称
        request_data = json.loads(request.body)
        job_name = request_data.get('jobname')

        if not job_name:
            return JsonResponse({"error": "Job name is required."}, status=400)

        server = jenkins_init()  # 初始化 Jenkins 服务器

        # 尝试触发 Jenkins 作业
        server.build_job(job_name)

        return JsonResponse({"message": f"Job '{job_name}' triggered successfully."}, status=200)

    except jenkins.NotFoundException:
        return JsonResponse({"error": f"Job '{job_name}' not found."}, status=404)
    except jenkins.JenkinsException as e:
        return JsonResponse({"error": str(e)}, status=500)
    except Exception as e:
        print('error: ', e)
        return JsonResponse({"error": "An unexpected error occurred."}, status=500)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_job(request):
    """Delete a Jenkins job."""

    try:
        request_data = json.loads(request.body)
        job_name = request_data.get('jobname')
        if not job_name:
            return JsonResponse({"error": "Job name is required."}, status=400)

        server = jenkins_init()
        server.delete_job(job_name)
        return JsonResponse({"message": f"Job '{job_name}' deleted."}, status=200)
    except jenkins.NotFoundException:
        return JsonResponse({"error": "Job not found."}, status=404)
    except jenkins.JenkinsException as e:
        return JsonResponse({"error": str(e)}, status=500)
    except Exception as e:
        return JsonResponse({"error": "An unexpected error occurred."}, status=500)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def select_job_one(request):
    """Select a Jenkins job."""

    try:
        request_data = json.loads(request.body)
        job_name = request_data.get('jobname')
        if not job_name:
            return JsonResponse({"error": "Job name is required."}, status=400)

        server = jenkins_init()
        data = server.get_job_name(job_name)
        print("get job: ", data)
        return JsonResponse({"message": f"Get Job '{job_name}' Success.", "data":f"{data}"}, status=200)

    except jenkins.NotFoundException:
        return JsonResponse({"error": "Job not found."}, status=404)

    except jenkins.JenkinsException as e:
        return JsonResponse({"error": str(e)}, status=500)

    except Exception as e:
        return JsonResponse({"error": "An unexpected error occurred."}, status=500)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def select_job_all(request):
    """Select a Jenkins job."""

    try:
        server = jenkins_init()
        jobs = server.get_all_jobs()
        return JsonResponse({"message": f"Get Job Success.","JobList": jobs}, status=200)

    except jenkins.JenkinsException as e:
        return JsonResponse({"error": str(e)}, status=500)

    except Exception:
        return JsonResponse({"error": "An unexpected error occurred."}, status=500)





@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stop_job(request):
    """Stop a Jenkins job."""

    request_data = json.loads(request.body)
    job_name = request_data.get('jobname')
    if not job_name:
        return JsonResponse({"error": "Job name is required."}, status=400)

    try:
        server = jenkins_init()
        server.stop_build(job_name)
        return JsonResponse({"message": f"Job '{job_name}' stopped successfully."}, status=200)
    except jenkins.NotFoundException:
        return JsonResponse({"error": "Job not found."}, status=404)
    except jenkins.JenkinsException as e:
        return JsonResponse({"error": str(e)}, status=500)
    except Exception as e:
        return JsonResponse({"error": "An unexpected error occurred."}, status=500)




def generate_pipeline_config_php(code_url, environment, deploy_host):
    """Generate the XML configuration for the Jenkins pipeline job."""
    return f'''
       <flow-definition plugin="workflow-job@2.40">
         <description>My Pipeline job</description>
         <keepDependencies>false</keepDependencies>
         <properties/>
         <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.93">
           <script>
pipeline {{
    agent {{
        node {{
            label 'master'
            customWorkspace "workspace/$JOB_NAME/$BUILD_NUMBER"
        }}
    }}

    options {{
        disableConcurrentBuilds()
        timeout(time: 240, unit: 'MINUTES')
    }}

    stages {{
        stage('Checkout Code') {{
            steps {{
                git url: '{code_url}', branch: 'main'
            }}
        }}
        stage('Hello') {{
            steps {{
                echo 'Hello World'
            }}
        }}
    }}

    post {{
        always {{
            script {{
                echo 'Hello always'
            }}
        }}
        success {{
            script {{
                echo 'Hello success'
            }}
        }}
        failure {{
            script {{
                echo 'Hello failure'
            }}
        }}
    }}
}}
           </script>
           <sandbox>true</sandbox>
         </definition>
         <triggers/>
         <disabled>false</disabled>
       </flow-definition>
    '''

def generate_pipeline_config_java(code_url, environment, deploy_host):
    """Generate the XML configuration for the Jenkins pipeline job."""
    return f'''
       <flow-definition plugin="workflow-job@2.40">
         <description>My Java Pipeline job</description>
         <keepDependencies>false</keepDependencies>
         <properties/>
         <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.93">
           <script>
pipeline {{
    agent {{
        node {{
            label 'master'
            customWorkspace "workspace/$JOB_NAME/$BUILD_NUMBER"
        }}
    }}

    options {{
        disableConcurrentBuilds()
        timeout(time: 240, unit: 'MINUTES')
    }}


    stages {{
        stage('Checkout Code') {{
            steps {{
                git url: '{code_url}', branch: 'main'
            }}
        }}
        stage('Hello') {{
            steps {{
                echo 'Hello World'
            }}
        }}
    }}

    post {{
        always {{
            script {{
                echo 'Hello always'
            }}
        }}
        success {{
            script {{
                echo 'Hello success'
            }}
        }}
        failure {{
            script {{
                echo 'Hello failure'
            }}
        }}
    }}
}}
           </script>
           <sandbox>true</sandbox>
         </definition>
         <triggers/>
         <disabled>false</disabled>
       </flow-definition>
    '''


def generate_pipeline_config_cpp(code_url, environment, deploy_host):
    """Generate the XML configuration for the Jenkins pipeline job."""
    return f'''
       <flow-definition plugin="workflow-job@2.40">
         <description>My C++ Pipeline job</description>
         <keepDependencies>false</keepDependencies>
         <properties/>
         <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.93">
           <script>
pipeline {{
    agent {{
        node {{
            label 'master'
            customWorkspace "workspace/$JOB_NAME/$BUILD_NUMBER"
        }}
    }}

    options {{
        disableConcurrentBuilds()
        timeout(time: 240, unit: 'MINUTES')
    }}


    stages {{
        stage('Checkout Code') {{
            steps {{
                git url: '{code_url}', branch: 'main'
            }}
        }}
        stage('Hello') {{
            steps {{
                echo 'Hello World'
            }}
        }}
    }}

    post {{
        always {{
            script {{
                echo 'Hello always'
            }}
        }}
        success {{
            script {{
                echo 'Hello success'
            }}
        }}
        failure {{
            script {{
                echo 'Hello failure'
            }}
        }}
    }}
}}
           </script>
           <sandbox>true</sandbox>
         </definition>
         <triggers/>
         <disabled>false</disabled>
       </flow-definition>
    '''


def generate_pipeline_config_static_web(code_url, environment, deploy_host):
    """Generate the XML configuration for the Jenkins pipeline job."""
    return f'''
       <flow-definition plugin="workflow-job@2.40">
         <description>My Static Web Pipeline job</description>
         <keepDependencies>false</keepDependencies>
         <properties/>
         <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.93">
           <script>
pipeline {{
    agent {{
        node {{
            label 'master'
            customWorkspace "workspace/$JOB_NAME/$BUILD_NUMBER"
        }}
    }}

    options {{
        disableConcurrentBuilds()
        timeout(time: 240, unit: 'MINUTES')
    }}


    stages {{
        stage('Checkout Code') {{
            steps {{
                git url: '{code_url}', branch: 'main'
            }}
        }}
        stage('Hello') {{
            steps {{
                echo 'Hello World'
            }}
        }}
    }}

    post {{
        always {{
            script {{
                echo 'Hello always'
            }}
        }}
        success {{
            script {{
                echo 'Hello success'
            }}
        }}
        failure {{
            script {{
                echo 'Hello failure'
            }}
        }}
    }}
}}
           </script>
           <sandbox>true</sandbox>
         </definition>
         <triggers/>
         <disabled>false</disabled>
       </flow-definition>
    '''



def create_job_if_not_exists(server, job_name, pipeline_config):
    """Create a Jenkins job if it doesn't already exist."""
    if not server.job_exists(job_name):
        server.create_job(job_name, pipeline_config)
        return True
    return False