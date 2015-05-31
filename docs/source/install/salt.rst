
=================
Salt Installation
=================

if your infrastucutre is managed by Salt use and contribute to our Salt Formula

https://github.com/django-leonardo/salt-formula-leonardo


.. code-bash:: bash

    salt-call state.sls leonardo

Sample pillar
=============

.. code-block:: yaml

    leonardo:
      server:
        enabled: true
        app:
          example_app:
          	site_name: 'My awesome site'
            enabled: true
            development: true
            workers: 3
            bind:
              address: 0.0.0.0
              port: 9754
              protocol: tcp
            source:
              type: 'git'
              address: 'git@repo1.robotice.cz:python-apps/leonardo.git'
              rev: 'master'
            secret_key: 'y5m^_^ak6+5(f.m^_^ak6+5(f.m^_^ak6+5(f.'
            database:
              engine: 'postgresql'
              host: '127.0.0.1'
              name: 'leonardo'
              password: 'db-pwd'
              user: 'leonardo'
            mail:
              host: 'mail.domain.com'
              password: 'mail-pwd'
              user: 'mail-user'
            admins:
              mail@majklk.cz:
                name: majklk 
              mail@newt.cz: {}
            managers:
              mail@majklk.cz:
                name: majklk 
              mail@newt.cz:
                name: newt
            plugin:
              eshop: {}
              static: {}
              sentry: {}
              my_site:
                site: true
              blog:
                source:
                  engine: 'git'
                  address: 'git+https://github.com/django-leonardo/leonardo-module-blog.git#egg=leonardo_module_blog'
            languages:
              en:
                default: true
              cs: {}
              de: {}

