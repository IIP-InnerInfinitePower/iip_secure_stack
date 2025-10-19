FROM nginx:stable
COPY conf.d/ /etc/nginx/conf.d/
EXPOSE 80
HEALTHCHECK CMD curl -fsS http://localhost/ || exit 1
