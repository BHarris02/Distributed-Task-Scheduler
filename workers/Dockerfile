FROM openjdk:17-jdk-slim

WORKDIR /app

COPY out/ ./out/
COPY libs/ ./libs/

CMD ["java", "-cp", "out:libs/*", "com.taskworker.Worker"]
