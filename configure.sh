#!/bin/bash

if [[ ! -d "nginx" ]]; then
     mkdir nginx
fi
if [[ ! -d "zip" ]]; then
     mkdir zip
fi
if [[ ! -d "postgres_data" ]]; then
     mkdir postgres_data
     docker compose restart postgres
fi
while read line; do export "$line"; done < .env
echo "START"

while read line; do echo "$line"; done < .env

echo ${CONTAINER_NAME}

EXISTE_DJANGO=$(docker ps | grep driver-new-tech)
EXISTE_CELERY=$(docker ps | grep driver-celery-${CONTAINER_NAME})
DJANGO_HOST="localhost"
if [ "${EXISTE_DJANGO}" != "" ]; then
     DJANGO_HOST=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' driver-new-tech)
fi
CELERY_HOST="localhost"
if [ "${EXISTE_CELERY}" != "" ]; then
     CELERY_HOST=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' driver-celery-${CONTAINER_NAME})
fi

cd /var/www/driver-new-tech
sudo cp driver-app.conf nginx/driver.conf
echo $CELERY_HOST
echo $DJANGO_HOST
echo "copied file from driver-app.conf"
sudo sed -i -e "s/HOST_NAME/${HOST_NAME}/g" /var/www/driver-new-tech/nginx/driver.conf
sudo sed -i -e "s/STATIC_ROOT/${STATIC_ROOT},g" /var/www/driver-new-tech/nginx/driver.conf
sudo sed -i -e "s/DIST_ROOT/${DIST_ROOT},g" /var/www/driver-new-tech/nginx/driver.conf
sudo sed -i -e "s/driver-new-tech/${DJANGO_HOST}/g" /var/www/driver-new-tech/nginx/driver.conf
sudo sed -i -e "s/driver-celery/${CELERY_HOST}/g" /var/www/driver-new-tech/nginx/driver.conf
sudo sed -i -e "s/windshaft/$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' windshaft)/g" /var/www/driver-new-tech/nginx/driver.conf

# sudo sed -i -e "s/HOST_NAME/${HOST_NAME}/g" nginx/driver.conf
# echo $HOST_NAME
# sudo sed -i -e "s,STATIC_ROOT,$STATIC_ROOT,g" nginx/driver.conf
# echo $STATIC_ROOT
# sudo sed -i -e "s,DIST_ROOT,$DIST_ROOT,g" nginx/driver.conf
# echo $DIST_ROOT
# echo "replacing variables"
# sudo sed -e "s/driver-new-tech/${DJANGO_HOST}/g" nginx/driver.conf
# echo $DJANGO_HOST
# sudo sed -e "s/driver-celery/${CELERY_HOST}/g" nginx/driver.conf
# echo $CELERY_HOST
# sudo sed -e "s/windshaft/$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' windshaft)/g" nginx/driver.conf
echo "replaced variables"

## sudo docker exec driver-nginx sed -i -e "s/HOST_NAME/${HOST_NAME}/g" /etc/nginx/conf.d/driver-app.conf

if [ $PROTOCOL == "http" ]
then
     echo "HTTP"
else
     echo "HTTPS"
 #    docker exec driver-nginx certbot
fi
if [ "${EXISTE_DJANGO}" != "" ]; then
     docker exec "driver-new-tech" ./manage.py collectstatic --noinput
     docker exec "driver-new-tech" ./manage.py migrate
     docker exec -it $(docker inspect -f '{{.ID}}' driver-new-tech) python manage.py createsuperuser
fi
if [ $STATIC_ROOT != $WINDSHAFT_FILES ]; then
     sudo cp -r static "$STATIC_ROOT/"
fi
##cd /var/www/driver-new-tech
##sudo mv nginx/driver.conf /etc/nginx/sites-enabled/default
sudo service nginx restart
##echo "Remember to run certbot now."
##docker compose restart driver-nginx
