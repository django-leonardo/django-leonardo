
======================
Leonardo in Production
======================

Leonardo in production is standard Django application. We use Gunicorn under Supervisor with Nginx proxy.

Supervisor
----------

.. code-block:: bash

    [program:leonardo_demo]
    command=/srv/leonardo/sites/demo/leonardo/contrib/gunicorn/server
    stdout_logfile=/srv/leonardo/sites/demo/logs/access.log
    stderr_logfile=/srv/leonardo/sites/demo/error.log
    user=leonardo
    autostart=true
    autorestart=true

Gunicorn
--------

.. code-block:: bash
    
    #!/bin/bash

    NAME="leonardo_demo"
    DJANGODIR=/srv/leonardo/sites/demo
    USER=leonardo
    GROUP=leonardo
    NUM_WORKERS=3
    DJANGO_SETTINGS_MODULE=leonardo.settings
    DJANGO_WSGI_MODULE=wsgi

    echo "Starting $NAME as `whoami`"

    # Activate the virtual environment
    cd $DJANGODIR
    source /srv/leonardo/sites/demo/bin/activate
    export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
    export PYTHONPATH=$DJANGODIR:$PYTHONPATH

    # Start your Django Unicorn
    # Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
    exec gunicorn ${DJANGO_WSGI_MODULE}:application \
      --name $NAME \
      --workers $NUM_WORKERS \
      --user=$USER --group=$GROUP \
      --log-level=debug \
      --bind=0.0.0.0:9754

for Tornado see Github page

Nginx
-----

.. code-block:: bash

    upstream leonardo_server_leonardo_demo {
        server localhost:9754 fail_timeout=0;
    }

    server {
      listen 80;

      server_name demo.cms.robotice.cz;

      client_max_body_size 20M;

      access_log  /var/log/nginx/demo-access;
      error_log   /var/log/nginx/demo-error;

      keepalive_timeout 5;

    gzip on;
    gzip_min_length  1100;
    gzip_buffers  4 32k;
    gzip_types    text/plain application/x-javascript text/xml text/css;
    gzip_vary on;

      location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;

        if (!-f $request_filename) {
          proxy_pass http://leonardo_server_leonardo_demo;
          break;
        }
      }

      location /static {
        autoindex on;
        alias /srv/leonardo/sites/demo/static;
        expires    30d;
     }

      location /media {
        autoindex on;
        alias /srv/leonardo/sites/demo/media;
        expires    30d;
      }

    }
