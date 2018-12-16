CWD=$(shell pwd)

VERSION = "1.0.6"
ORGANIZATION ?= "cznewt"

help:
	@echo "Available actions:"
	@echo "  build         Build django-leonardo docker container"
	@echo "  publish       Publish django-leonardo docker container"
	@echo "  doc           Build project documentation"

all: build publish

build:
	docker build --no-cache -t $(ORGANIZATION)/django-leonardo:$(VERSION) -f ./Dockerfile .
	docker tag $(ORGANIZATION)/django-leonardo:$(VERSION) $(ORGANIZATION)/django-leonardo:latest

publish:
	docker push $(ORGANIZATION)/django-leonardo:$(VERSION)
	docker push $(ORGANIZATION)/django-leonardo:latest
