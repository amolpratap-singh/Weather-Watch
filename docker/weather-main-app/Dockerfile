# Used Offical Python runtime as a base image
FROM python:3.11


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

# Define environment variable
ENV LOG_LEVEL=INFO PROCESS_INTRVAL=30

# Make port 80 available to the world outside this container
#EXPOSE 5000 8080
# Run app.py when the container launches
CMD ["python3", "/app/src/main.py"]
#CMD ["python3", "/app/src/test.py"]

LABEL org.opencontainers.image.version="$TAG"
