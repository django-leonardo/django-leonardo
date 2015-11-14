FROM ubuntu:14.04
MAINTAINER Michael Kuty "mail@michaelkuty.eu"
RUN apt-get -qq update
RUN apt-get install -y python-dev python-setuptools supervisor git-core libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev
RUN easy_install pip
RUN pip install virtualenv
RUN pip install uwsgi
RUN virtualenv --no-site-packages /opt/leonardo
ADD . /opt/apps/leonardo
ADD /contrib/supervisor/docker.conf /opt/supervisor.conf
ADD /contrib/supervisor/run.sh /usr/local/bin/run
RUN /opt/leonardo/bin/pip install -e git+https://github.com/django-leonardo/django-leonardo.git@develop#egg=django_leonardo
RUN (cd /opt/apps/leonardo && /opt/leonardo/bin/django-admin startproject --template=https://github.com/django-leonardo/site-template/archive/master.zip myproject)
RUN export PYTHONPATH=/opt/apps/leonardo/myproject
ADD /contrib/django/manage.py /opt/apps/leonardo/manage.py
RUN (/opt/leonardo/bin/python /opt/apps/leonardo/myproject/manage.py makemigrations --noinput)
RUN (/opt/leonardo/bin/python /opt/apps/leonardo/myproject/manage.py migrate --noinput)
RUN (/opt/leonardo/bin/python /opt/apps/leonardo/myproject/manage.py collectstatic --noinput)
EXPOSE 8000
CMD ["/bin/sh", "-e", "/usr/local/bin/run"]
