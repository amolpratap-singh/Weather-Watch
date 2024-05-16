# Used Offical Python runtime as a base image
FROM python:3.12

ARG TAG
ENV TAG ${TAG:-latest}

RUN mkdir -p /app

# Working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY weather-main-app/ /app
COPY weather-main-app/requirements.txt /app/

# Install dependencies specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3.12", "/app/src/main.py"]

LABEL org.opencontainers.image.version="$TAG"
