# Docker image for Weather API Server

# Build arguments
ARG SWAGGER_CODEGEN=https://github.com/swagger-api/swagger-codegen/archive/
ARG SWAGGER_VERSION=swagger-codegen-3.0.35
ARG SWAGGER_PACKAGE=v3.0.35.tar.gz
ARG SWAGGER_CODEGEN_BUILD_REPO=/usr/local/codegen_build

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

# Final Layer
FROM openjdk:11-jdk-slim

ARG SWAGGER_VERSION
ARG SWAGGER_CODEGEN_BUILD_REPO

COPY --from=swagger_builder ${SWAGGER_CODEGEN_BUILD_REPO}/${SWAGGER_VERSION} /opt/swagger-codegen

WORKDIR /opt/swagger-codegen

# Define entry point or default command if needed
# ENTRYPOINT ["java", "-jar", "swagger-codegen-cli.jar"]

# Clean up Maven and other unnecessary files if needed
# RUN apt-get remove --purge -y maven \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*
