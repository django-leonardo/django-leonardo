FROM leonardocms/ubuntu:14.04
MAINTAINER Michael Kuty "mail@michaelkuty.eu"
RUN apt-get update
RUN apt-get install supervisor git git-core -y
RUN easy_install pip
RUN pip install gunicorn psycopg2 Whoosh python-memcached
RUN pip install git+https://github.com/django-leonardo/django-leonardo.git#egg=django_leonardo
RUN pip install leonardo-system==0.0.8.post4
RUN mkdir -p /usr/lib/leonardo/myproject
RUN (django-admin startproject --template=https://github.com/django-leonardo/site-template/archive/docker.zip myproject /usr/lib/leonardo/myproject)
RUN export PYTHONPATH=/usr/lib/leonardo/myproject
