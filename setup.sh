docker-compose run django bash -c "service mongodb start && cd SOM_PROJECT && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8080"
