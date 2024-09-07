# syntax=docker/dockerfile:1
FROM python:3.12-alpine

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Set the working directory
WORKDIR /app

# Command to run the bot (make sure you have a file like bot.py or similar)
CMD ["python", "bot.py"]
