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
FROM ubuntu:latest as builder

ARG API_SERVER_BUILD
ARG SWAGGER_VERSION
ARG SWAGGER_CODEGEN_BUILD_REPO

# Java 11 and Python 3.12 installation
RUN apt-get update && \
 apt-get install -y openjdk-11-jdk && \
 apt-get install -y python3.12 && \
 apt-get clean;

# Set the default Java and Python versions
RUN update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-11-openjdk-amd64/bin/java 1 && \
 update-alternatives --set java /usr/lib/jvm/java-11-openjdk-amd64/bin/java && \
 update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 && \
 update-alternatives --set python3 /usr/bin/python3.12

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$PATH:$JAVA_HOME/bin"

RUN mkdir -p ${API_SERVER_BUILD}

WORKDIR ${API_SERVER_BUILD}

COPY build_src ${API_SERVER_BUILD}/build_src
COPY weather-api-server/src/controllers ${API_SERVER_BUILD}/src/controllers
COPY weather-api-spec ${API_SERVER_BUILD}/weather-api-spec
COPY --from=swagger_builder ${SWAGGER_CODEGEN_BUILD_REPO}/${SWAGGER_VERSION}/modules/swagger-codegen-cli/target/swagger-codegen-cli.jar swagger-codegen-cli.jar

RUN /usr/bin/python3.12 build_src/build.py



#FROM openjdk:11-jdk-slim as builder

#ARG SWAGGER_VERSION
#ARG SWAGGER_CODEGEN_BUILD_REPO

#COPY --from=swagger_builder ${SWAGGER_CODEGEN_BUILD_REPO}/${SWAGGER_VERSION} /opt/swagger-codegen

#WORKDIR /opt/swagger-codegen

# Define entry point or default command if needed
# ENTRYPOINT ["java", "-jar", "swagger-codegen-cli.jar"]

# Clean up Maven and other unnecessary files if needed
# RUN apt-get remove --purge -y maven \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*
