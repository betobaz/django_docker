# django_docker
Proyecto de prueba para desarrollo de django

Primero este

docker-compose -f dev.yml build

Luego este

docker-compose -f dev.yml up

docker-compose -f dev.yml run django python manage.py makemigrations

docker-compose -f dev.yml run django python manage.py migrate

docker-compose -f dev.yml run django python manage.py createsuperuser

