FROM nginx

RUN rm -rf /etc/nginx/conf.d/default.conf 

COPY Dockerfiles/nginx/nginxapp.conf /etc/nginx/conf.d/flaskapp.conf
EXPOSE 80