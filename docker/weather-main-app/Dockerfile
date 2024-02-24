# Used Offical Python runtime as a base image
FROM python:3.12

ARG TAG
ENV TAG ${TAG:-latest}

# Add entry to /etc/hosts
# RUN echo "172.19.0.2 opensearch" >> /etc/hosts

# Copy the script into the container
COPY docker/weather-main-app/add_host_entry.sh /usr/local/bin/

RUN mkdir -p /app

# Working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY docker/weather-main-app/ /app
COPY docker/weather-main-app/requirements.txt /app/

# Install dependencies specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Define environment variable
ENV LOG_LEVEL=INFO PROCESS_INTRVAL=30

# Make port 80 available to the world outside this container
#EXPOSE 5000 8080

# Execute the script at runtime
ENTRYPOINT ["/usr/local/bin/add_host_entry.sh"]

# Run app.py when the container launches
CMD ["python3", "/app/src/main.py"]
# CMD ["python3", "/app/src/test.py"]

LABEL org.opencontainers.image.version="$TAG"
