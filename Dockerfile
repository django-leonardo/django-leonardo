FROM leonardocms/ubuntu:14.04
MAINTAINER Michael Kuty "mail@michaelkuty.eu"
RUN apt-get install git-core supervisor -y
RUN virtualenv --no-site-packages /opt/leonardo
ADD . /usr/lib/leonardo/bin/activate
RUN /usr/lib/leonardo/bin/pip install uwsgi
RUN /usr/lib/leonardo/bin/pip install -e git+https://github.com/django-leonardo/django-leonardo.git@feature/debian_docker#egg=django_leonardo
RUN (cd /usr/lib/leonardo && /usr/lib/leonardo/bin/django-admin startproject --template=https://github.com/django-leonardo/site-template/archive/master.zip myproject)
ADD /usr/lib/leonardo/src/django-leonardo/contrib/supervisor/docker.conf /opt/supervisor.conf
ADD /usr/lib/leonardo/src/django-leonardo/contrib/supervisor/run.sh /usr/local/bin/run
ADD /usr/lib/leonardo/src/django-leonardo/contrib/django/wsgi.py /usr/lib/leonardo/wsgi.py
RUN export PYTHONPATH=/usr/lib/leonardo/myproject
ADD /usr/lib/leonardo/src/django-leonardo/contrib/django/manage.py /usr/lib/leonardo/myproject/manage.py
RUN (/usr/lib/leonardo/bin/python /usr/lib/leonardo/myproject/manage.py makemigrations --noinput)
RUN (/usr/lib/leonardo/bin/python /usr/lib/leonardo/myproject/manage.py migrate --noinput)
RUN (cd /usr/lib/leonardo; /usr/lib/leonardo/bin/python /usr/lib/leonardo/myproject/manage.py collectstatic --noinput)
EXPOSE 8000
CMD ["/bin/sh", "-e", "/usr/local/bin/run"]
