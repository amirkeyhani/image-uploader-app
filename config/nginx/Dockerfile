FROM nginx:alpine
LABEL MAINTAINER="Amir Keyhani | https://amir.key_"

RUN rm /etc/nginx/conf.d/default.conf
ADD nginx.conf /etc/nginx/conf.d/
# COPY nginx.conf /etc/nginx/conf.d/default.conf
# EXPOSE 80

CMD nginx -g daemon off;