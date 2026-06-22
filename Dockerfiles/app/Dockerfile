FROM python:3.12-alpine
#creates a directory inside container naming app 
WORKDIR /app
#copies everthing from source_code's req  to current directory
COPY source_code/requirements.txt .
#--no-cache-dir will stop pip to store downloaded packages inside the image-makes smaller & cleaner image
RUN pip install --no-cache-dir -r requirements.txt
#any changes done in code will not again & again install req ,will reuse cached layer-becomes faster to deliver
COPY source_code/ .

ENTRYPOINT ["python", "server.py"]
