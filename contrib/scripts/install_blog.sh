#!/bin/bash

virtualenv -p /usr/bin/python2.7 leonardo_venv
cd leonardo_venv
. $PWD/bin/activate

pip install -e git+https://github.com/django-leonardo/django-leonardo@develop#egg=django-leonardo
pip install -r $PWD/src/django-leonardo/requirements.txt
pip install -e git+https://github.com/leonardo-modules/leonardo-module-blog#egg=leonardo_module_blog
pip install -r $PWD/src/leonardo_store/requirements.txt

django-admin startproject --template=https://github.com/django-leonardo/site-template/archive/master.zip myproject

export PYTHONPATH=$PWD/myproject
cd myproject

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py bootstrap_site --url=http://raw.githubusercontent.com/django-leonardo/django-leonardo/develop/contrib/bootstrap/blog.yaml

echo "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'mail@leonardo.cz', 'admin')" | python manage.py shell

python manage.py runserver 0.0.0.0:80

