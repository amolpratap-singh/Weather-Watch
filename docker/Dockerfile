# Docker image for Weather API Server

# Build arguments
ARG SWAGGER_CODEGEN=https://github.com/swagger-api/swagger-codegen/archive/
ARG SWAGGER_VERSION=swagger-codegen-3.0.35
ARG SWAGGER_PACKAGE=v3.0.35.tar.gz
ARG SWAGGER_CODEGEN_BUILD_REPO=/usr/local/codegen_build
ARG API_SERVER_BUILD=/usr/local/api_server

# Swagger Codegen Build Layer
FROM maven:3.8.1-jdk-11 as swagger_builder

ARG SWAGGER_CODEGEN
ARG SWAGGER_PACKAGE
ARG SWAGGER_VERSION
ARG SWAGGER_CODEGEN_BUILD_REPO

RUN mkdir -p ${SWAGGER_CODEGEN_BUILD_REPO}
WORKDIR ${SWAGGER_CODEGEN_BUILD_REPO}

RUN wget -nv ${SWAGGER_CODEGEN}${SWAGGER_PACKAGE} \
 && tar -xvzf ${SWAGGER_CODEGEN_BUILD_REPO}/${SWAGGER_PACKAGE}

WORKDIR ${SWAGGER_CODEGEN_BUILD_REPO}/${SWAGGER_VERSION}

RUN mvn clean package

# Second Layer with swagger codegen controller generation
# FROM ubuntu:20.04 as builder
FROM ubuntu:latest as builder

ARG API_SERVER_BUILD
ARG SWAGGER_VERSION
ARG SWAGGER_CODEGEN_BUILD_REPO

# Java 11 installation
RUN apt-get update && \
 apt-get install -y openjdk-11-jdk && \
 apt-get clean;

# Set the default Java and Python versions
#RUN update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-11-openjdk-amd64/bin/java 1 && \
# update-alternatives --set java /usr/lib/jvm/java-11-openjdk-amd64/bin/java && \
# update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 && \
# update-alternatives --set python3 /usr/bin/python3.12

# Update the package lists and install required packages
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-distutils python3.11-venv python3.11-dev && \
    apt-get clean;

RUN apt-get install -y curl && \
 apt-get clean;

# Install pip for Python 3.12
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.11 get-pip.py && \
    rm get-pip.py

# Install any Python packages using pip3
COPY requirements.txt /tmp
RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$PATH:$JAVA_HOME/bin"

RUN mkdir -p ${API_SERVER_BUILD}

WORKDIR ${API_SERVER_BUILD}

COPY build_src ${API_SERVER_BUILD}/build_src
COPY weather-api-server-app/src/controllers ${API_SERVER_BUILD}/src/controllers
COPY weather-api-spec ${API_SERVER_BUILD}/weather-api-spec
COPY --from=swagger_builder ${SWAGGER_CODEGEN_BUILD_REPO}/${SWAGGER_VERSION}/modules/swagger-codegen-cli/target/swagger-codegen-cli.jar build_src/swagger-codegen-cli.jar

RUN /usr/bin/python3.11 build_src/build.py

RUN mv ${API_SERVER_BUILD}/build_src/src/swagger_server ${API_SERVER_BUILD}/swagger_server
COPY weather-api-server-app/src/*.py ${API_SERVER_BUILD}/swagger_server
COPY weather-api-server-app/src/utils ${API_SERVER_BUILD}/utils
COPY app.py ${API_SERVER_BUILD}

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000","swagger_server.wsgi:app", "--worker-class", "uvicorn.workers.UvicornWorker"]