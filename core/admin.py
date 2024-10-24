# 在你的项目的 admin.py 文件中，确保包含以下内容

from django.contrib import admin

# 自定义站点标题和标签栏标题
admin.site.site_header = "自动化部署平台后台管理"  # 页面顶部的标题
admin.site.site_title = "自动化部署平台"  # 浏览器标签栏标题
admin.site.index_title = "自动化部署平台首页"  # 管理首页的标题
