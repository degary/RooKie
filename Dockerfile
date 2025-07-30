FROM python:3.13.5-slim

WORKDIR /app

# 设置环境变量
ENV DJANGO_ENV=prod
ENV PYTHONUNBUFFERED=1

# 更换apt源为阿里云镜像
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ gunicorn psycopg2-binary

COPY . .

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 创建启动脚本
RUN echo '#!/bin/bash\n\
python manage.py migrate\n\
exec gunicorn -c gunicorn.conf.py Rookie.wsgi:application' > /app/start.sh
RUN chmod +x /app/start.sh

# 安装netcat用于检查数据库连接
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

CMD ["/app/start.sh"]
