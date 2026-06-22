FROM nginx

RUN rm -rf /etc/nginx/conf.d/default.conf 

COPY nginxapp.conf /etc/nginx/conf.d/flaskapp.conf
EXPOSE 80