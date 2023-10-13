jupyter-compose-build-no-cache:
	docker-compose --compatibility build --no-cache

jupyter-compose:
	docker-compose --compatibility build
	docker-compose -f docker-compose.yml --compatibility up

jupyter-compose-background:
	docker-compose --compatibility build
	docker-compose -f docker-compose.yml --compatibility up -d

jupyter-stop:
	docker-compose -f docker-compose.yml down

attach:
	docker exec -i -t wanglab-jupyter-qiime2 /bin/bash