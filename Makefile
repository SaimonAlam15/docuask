dev:
	docker compose -f compose.yml -f compose.dev.yml up --build

prod:
	docker compose up --build

dev-down:
	docker compose -f compose.yml -f compose.dev.yml down

prod-down:
	docker compose down

logs:
	docker compose logs -f