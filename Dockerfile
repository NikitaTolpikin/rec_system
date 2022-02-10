FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN apt-get update \
    && apt-get install -y binutils libproj-dev gdal-bin \
    && pip install -r requirements.txt
COPY . /code
CMD ["bash", "/code/run.sh"]
