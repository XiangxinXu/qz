#!/bin/sh
# 后台启动
python3 -D manage.py runserver 0.0.0.0:8000
# 关闭后台启动，hold住进程
nginx -g 'daemon off;'

