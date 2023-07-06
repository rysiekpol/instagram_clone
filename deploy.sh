#!/bin/bash

ssh -o StrictHostKeyChecking=no -i $ID_RSA $SERVER_USER@$SERVER_IP -p $SERVER_PORT << 'ENDSSH'
	cd /home/flask
	export $(cat .env | xargs)

	docker login -u $CI_REGISTRY_USER -p $CI_JOB_TOKEN $CI_REGISTRY
	docker pull $IMAGE:instagram || true
	docker pull $IMAGE:nginx || true
	docker compose -f docker-compose.ci.yml up -d --build
ENDSSH