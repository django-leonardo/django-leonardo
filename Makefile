CWD=$(shell pwd)

VERSION = "1.0.7"
ORGANIZATION ?= "cznewt"

help:
	@echo "Available actions:"
	@echo "  build         Build base django-leonardo docker container"
	@echo "  publish       Publish base django-leonardo docker container"

all: build publish

build:
	docker build --no-cache -t $(ORGANIZATION)/django-leonardo:$(VERSION) -f ./Dockerfile .
	docker tag $(ORGANIZATION)/django-leonardo:$(VERSION) $(ORGANIZATION)/django-leonardo:latest

publish:
	docker push $(ORGANIZATION)/django-leonardo:$(VERSION)
	docker push $(ORGANIZATION)/django-leonardo:latest
