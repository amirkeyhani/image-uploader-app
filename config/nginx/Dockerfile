FROM nginx:1.21.6
LABEL MAINTAINER="Amir Keyhani | https://amir.key_"

COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]