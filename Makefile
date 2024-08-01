dbcreate:
	docker run -d \
	--name my-postgres \
	-e POSTGRES_USER=postgres \
	-e POSTGRES_PASSWORD=postgres \
	-e POSTGRES_DB=lite \
	-p 5432:5432 \
	-v postgres_data:/var/lib/postgresql/data \
	--network api-net \
	postgres:15-alpine


buildapi:
	docker build -t api .

runapi:
	docker run --rm -p 8000:8000 -d --network api-net --name api api
