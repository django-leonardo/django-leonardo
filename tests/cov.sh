#!/bin/sh
coverage run --branch --include="*leonardo/leonardo*" ./manage.py test testapp
coverage html