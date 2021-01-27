THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help dev prod up start down destroy stop restart
comma = ,

help:
		@echo ""
		@echo "make dev"
		@echo ""

dev:
		docker-compose up -d postgres
		sleep 15
		docker-compose up -d main_app
