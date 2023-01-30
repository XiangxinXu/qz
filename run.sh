#!/bin/sh
# 后台启动
nohup python3 manage.py runserver 0.0.0.0:8000 &
# 关闭后台启动，hold住进程
nginx -g 'daemon off;'

