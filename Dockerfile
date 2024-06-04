# Use the official Python image from the Docker Hub
FROM python:3.12.3-alpine3.20

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies and additional tools
RUN apk update && apk add --no-cache \
    build-base \
    gcc \
    libffi-dev \
    musl-dev \
    openssl-dev \
    postgresql-dev \
    vim \
    curl \
    inetutils-telnet

# Copy the rest of the application code to the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1