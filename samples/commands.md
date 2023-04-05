## Test locally
python3 NDVI_bacalhau.py

## Build Docker image
```
docker build -t jsolly/ndvi-bacalhau .
docker buildx build --platform linux/amd64 -t jsolly/ndvi-bacalhau-amd64 .
```

## Test Docker image locally
```
docker run --rm -v $PWD/inputs:/project/inputs jsolly/ndvi-bacalhau
```

## Publish to Docker Hub
```shell
docker login
docker push jsolly/ndvi-bacalhau-amd64
```

## Run on Bacalhau
First Upload inputs to IPFS
```shell
$ bacalhau docker run -v QmYKyYY1XX4SLX6jmpGEc8dnU5od6AALEwkigRVGej2kht:/project/inputs jsolly/ndvi-bacalhau-amd64:latest
```