##########
# Docker #
##########

.PHONY: d-up
d-up:
	docker-compose up -d

.PHONY: d-down
d-down:
	docker-compose down

.PHONY: d-restart
d-restart:
	docker-compose restart

.PHONY: d-python
d-python:
	docker-compose exec python-generator bash

#############
# Generator #
#############

.PHONY: generator
generator:
	docker-compose run --rm -p 3001:5000 -w /code python-generator python generator.py

.PHONY: train
train:
	docker-compose run --rm -w /code python-generator python train.py

.PHONY: tensorboard
tensorboard:
	docker-compose run --rm -p 3002:6006 -w /code python-generator tensorboard --logdir logs/tensorboard --bind_all

.PHONY: clear
clear:
	docker-compose run --rm -w /code python-generator rm -rf logs/*

.PHONY: tests
tests:
	docker-compose run --rm -w /code python-generator python -m unittest discover . "*Test.py"
