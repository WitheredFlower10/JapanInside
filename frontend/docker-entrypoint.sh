#!/bin/sh
set -e

BACKEND_URL=${BACKEND_URL:-http://backend:8000}

# Le but de ce script est de remplacer ${BACKEND_URL} dans le fichier de configuration Nginx par la valeur de l'environnement BACKEND_URL
envsubst '${BACKEND_URL}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

cat /etc/nginx/conf.d/default.conf

exec nginx -g 'daemon off;'

