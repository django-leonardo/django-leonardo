CWD=$(shell pwd)
APP_NAME=$(shell pwd | sed -e 's/\//:/g' | cut -d: -f5)

VERSION = "1.0.8"
ORGANIZATION ?= "cznewt"

help:
	@echo "Available actions:"
	@echo "  build               Build base django-leonardo docker container"
	@echo "  publish             Publish base django-leonardo docker container"
	@echo "  update_static       Compress static and sync templates."
	@echo "  update_templates    Sync templates without compress."

all: build publish

build:
	docker build --no-cache -t $(ORGANIZATION)/django-leonardo:$(VERSION) -f ./Dockerfile .
	docker tag $(ORGANIZATION)/django-leonardo:$(VERSION) $(ORGANIZATION)/django-leonardo:latest

publish:
	docker push $(ORGANIZATION)/django-leonardo:$(VERSION)
	docker push $(ORGANIZATION)/django-leonardo:latest

update_static:
	@if [ -d $(CWD)/../src/leonardo-theme-$(APP_NAME) ]; then \
    cd $(CWD)/../src/leonardo-theme-$(APP_NAME); git pull -r; \
    echo "CWD = "$(CWD); . $(CWD)/../bin/activate; python $(CWD)/../manage.py sync_all -f; \
  else \
    echo "Theme leonardo-theme-$(APP_NAME) not found.";\
  fi

update_templates:
	@if [ -d $(CWD)/../src/leonardo-theme-$(APP_NAME) ]; then \
    cd $(CWD)/../src/leonardo-theme-$(APP_NAME); git pull -r; \
    echo "CWD = "$(CWD); . $(CWD)/../bin/activate; python $(CWD)/../manage.py sync_all -f --nocompress; \
  else \
    echo "Theme leonardo-theme-$(APP_NAME) not found.";\
  fi
