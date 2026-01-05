.PHONY: help build run test clean seed crud-test

help:
	@echo "Available targets:"
	@echo "  build       - Build Docker image"
	@echo "  run         - Run Docker container locally"
	@echo "  test        - Test API endpoints with curl"
	@echo "  seed        - Seed database with sample books"
	@echo "  crud-test   - Run full CRUD test suite"
	@echo "  clean       - Stop and remove Docker container"

build:
	cd app && docker build -t bookstore-api:latest .

run:
	@echo "Starting container with environment variables from .env"
	@echo "Make sure you have MONGO_URI set in your environment or .env file"
	docker run -d \
		--name bookstore-api \
		-p 5001:5000 \
		--env-file app/.env \
		bookstore-api:latest

test:
	@echo "Testing /health endpoint..."
	@curl -s http://localhost:5001/health | python3 -m json.tool || curl -s http://localhost:5001/health
	@echo "\nTesting GET /books..."
	@curl -s http://localhost:5001/books | python3 -m json.tool | head -30 || curl -s http://localhost:5001/books

seed:
	cd scripts && python seed.py

crud-test:
	cd scripts && python crud_test.py

clean:
	docker stop bookstore-api || true
	docker rm bookstore-api || true

