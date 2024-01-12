# ifneq (,$(wildcard .env))
# 	$(info Found .env file.)
# 	include .env
# 	export
# endif

export PYTHONPATH := $(shell pwd):$(PYTHONPATH)

style:
	poetry run flake8 tld2

types:
	poetry run mypy tld2

check:
	make -j3 style types
