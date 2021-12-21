# Minimal Gallery Demo
 
 This is a very minimal demo created according to the [wagtail's getting started](https://docs.wagtail.io/en/stable/getting_started/) guide:
 
 ```sh
wagtail start mysite
 
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
 ```
 
The `HomePage` was replaced by a simple `Page` inheriting from `ImageGalleryMixin`.
