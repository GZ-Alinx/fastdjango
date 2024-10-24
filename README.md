# Django快速开发基础代码
## 1. 创建项目
```shell
django-admin startproject mysite
```
## 2. 创建应用
```shell
python manage.py startapp myapp
```
## 3. 创建数据库
```shell
python manage.py makemigrations
python manage.py migrate
```
## 4. 创建超级用户
```shell
python manage.py createsuperuser
```
## 5. 启动服务
```shell
python manage.py runserver
```
## 6. 访问接口文档
```
http://127.0.0.1:8000/swagger/
```
