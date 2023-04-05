FROM osgeo/gdal
RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install rasterio
RUN python3 -m pip install matplotlib

LABEL maintainer="jsolly"
RUN mkdir -p /project/outputs
RUN mkdir -p /project/inputs
WORKDIR /project
COPY ./NDVI_bacalhau.py /project/NDVI_bacalhau.py


CMD ["python3", "NDVI_bacalhau.py"]