docker run -d --name postgresql \
-p 5432:5432 \
-e POSTGRES_PASSWORD=postgres \
postgres:15