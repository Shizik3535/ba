dbcreate:
	docker run -d \
	--name my-postgres \
	-e POSTGRES_USER=postgres \
	-e POSTGRES_PASSWORD=postgres \
	-e POSTGRES_DB=lite \
	-p 5432:5432 \
	-v postgres_data:/var/lib/postgresql/data \
	postgres:15-alpine