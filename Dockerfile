# 使用官方 Python 作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量，防止 Python 生成 .pyc 文件，且让 stdout 和 stderr 无缓冲
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖项（如果需要）
# 例如，如果某些 Python 包需要编译工具，可以取消注释以下行
# RUN apt-get update && apt-get install -y build-essential

# 复制 requirements.txt 并安装 Python 依赖
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 复制应用代码到容器中
COPY . .

# 暴露 Gradio 默认端口
EXPOSE 7860

# 设置容器启动时运行的命令
CMD ["python", "app.py"]
