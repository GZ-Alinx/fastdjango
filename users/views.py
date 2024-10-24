# Create your views here.
# users/views.py
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework import status




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    修改密码接口:
    请求体应包含以下 JSON 数据:
    {
      "username": "", 
      "old_password": "oldpass", 
      "new_password1": "newpass123", 
      "new_password2": "newpass123"
    }
    """

    # 从请求体中获取用户名
    username = request.data.get("username")

    try:
        # 通过用户名查找用户对象
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

    # 使用找到的用户对象和请求数据创建 PasswordChangeForm
    form = PasswordChangeForm(user, request.data)

    if form.is_valid():
        form.save()
        update_session_auth_hash(request, user)  # 更新 session 避免用户被登出
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    """
    {"username": "newuser", "password": "password123", "email": "newuser@example.com"}
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password:
        return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"detail": "User with this username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_info(request):
    """
    {"username": "newusername", "email": "newemail@example.com", "first_name": "John", "last_name": "Doe"}
    """
    user = request.user
    data = request.data

    # 更新用户名
    if 'username' in data:
        if User.objects.filter(username=data['username']).exclude(id=user.id).exists():
            return Response({"detail": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
        user.username = data['username']

    # 更新邮箱
    if 'email' in data:
        if User.objects.filter(email=data['email']).exclude(id=user.id).exists():
            return Response({"detail": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)
        user.email = data['email']

    # 更新其他信息 (可扩展)
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']

    # 保存更新后的用户信息
    user.save()

    return Response({"detail": "User information updated successfully."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_all(request):
    queryset = User.objects.all()
    user_data = []

    for user in queryset:
            user_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            })

    return Response(user_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_users_one(request):
    try:
        # 获取请求体中的 username
        username = request.data.get("username")
        
        if not username:
            return Response({"message": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 查询用户对象
        user = User.objects.get(username=username)
        
        # 返回用户信息
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            # 你可以根据需要返回其他字段
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"message": f"Error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_users(request):
    """
    {"username":"ling"}
    """
    try:
        # 从请求数据中获取用户名
        username = request.data.get("username")

        if not username:
            return Response({'message': "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取用户对象
        userinfo = User.objects.get(username=username)
        userinfo.delete()
        return Response({'message': "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except User.DoesNotExist:
        return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': "Error occurred while deleting user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)