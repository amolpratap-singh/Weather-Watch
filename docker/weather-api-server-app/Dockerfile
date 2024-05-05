# Docker image for Weather API Server

FROM openjdk:11-jdk-slim as builder1

WORKDIR /app


COPY swagger-codegen-cli.jar /app/swagger-codegen-cli.jar

ENTRYPOINT ["java", "-jar", "/app/swagger-codegen-cli.jar"]
