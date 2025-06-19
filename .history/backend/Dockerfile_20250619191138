# backend/Dockerfile

# Use an official Python runtime as a parent image.
# 'slim' is a smaller version, great for production.
FROM python:3.9-slim

# Set the working directory inside the container to /app.
WORKDIR /app

# Copy the requirements file into the container.
COPY requirements.txt .

# Install any needed packages specified in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application code into the container.
COPY . .

# Command to run the application.
# Gunicorn is a production-ready web server for Python.
# It listens on all network interfaces (0.0.0.0) on port 5000.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
