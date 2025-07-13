start:
	docker-compose up -d

stop:
	docker-compose stop

restart:
	make stop
	make start

rebuild:
	docker-compose up -d --build --remove-orphans

l-mqtt:
	docker exec -it mqtt sh

l-ha:
	docker exec -it homeassistant bash

l-pai:
	docker exec -it pai bash

l-player:
	docker exec -it player bash

l-cloudflared:
	docker exec -it cloudflared bash
