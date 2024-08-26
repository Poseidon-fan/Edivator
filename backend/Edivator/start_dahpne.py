import os
import django
import sys
from daphne.cli import CommandLineInterface

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Edivator.settings')

# 初始化 Django 应用
django.setup()

# 启动 Daphne 服务器
sys.argv = ['daphne', '-b', '0.0.0.0', '-p', '8000', 'Edivator.asgi:application']
CommandLineInterface.entrypoint()
