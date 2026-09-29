dev:
	docker compose -f compose.yaml -f compose.dev.yaml up --build

prod:
	docker compose up --build

dev-down:
	docker compose -f compose.yaml -f compose.dev.yaml down

prod-down:
	docker compose down

logs:
	docker compose logs -f