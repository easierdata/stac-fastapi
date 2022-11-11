podman pod create --name app-pgstac -p 8080:8080 -p 5439:5432 -p 8082:8082

podman build -f Dockerfile -t docker.io/stac-utils/stac-fastapi

podman run \
-d --pod=app-pgstac \
-e POSTGRES_USER=username \
-e POSTGRES_PASSWORD=password \
-e POSTGRES_DB=postgis \
-e PGUSER=username \
-e PGPASSWORD=password \
-e PGHOST=localhost \
-e PGDATABASE=postgis \
--name=stac-db ghcr.io/stac-utils/pgstac:v0.6.10 

#bash -c "postgres -N 500"


podman run \
--pod=app-pgstac \
-e APP_HOST=0.0.0.0 \
-e APP_PORT=8082 \
-e RELOAD=true \
-e ENVIRONMENT=local \
-e POSTGRES_USER=username \
-e POSTGRES_PASS=password \
-e POSTGRES_DBNAME=postgis \
-e POSTGRES_HOST_READER=database \
-e POSTGRES_HOST_WRITER=database \
-e POSTGRES_PORT=5432 \
-e WEB_CONCURRENCY=10 \
-e VSI_CACHE=TRUE \
-e GDAL_HTTP_MERGE_CONSECUTIVE_RANGES=YES \
-e GDAL_DISABLE_READDIR_ON_OPEN=EMPTY_DIR \
-e DB_MIN_CONN_SIZE=1 \
-e DB_MAX_CONN_SIZE=1 \
-e USE_API_HYDRATE=${USE_API_HYDRATE:-false} \
-v ./stac_fastapi:/app/stac_fastapi:Z \
-v ./scripts:/app/scripts:Z \
--name stac-fastapi-pgstac docker.io/stac-utils/stac-fastapi bash -c "./scripts/wait-for-it.sh database:5432 && python -m stac_fastapi.pgstac.app"
#
podman run --rm docker.io/stac-utils/stac-fastapi bash -c "./scripts/wait-for-it.sh app-pgstac:8082 -- python /app/scripts/ingest_joplin.py http://app-pgstac:8082 "