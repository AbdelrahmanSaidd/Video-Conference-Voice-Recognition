# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Define environment variable
ENV NAME World
# Expose port 5000 to the outside world
EXPOSE 5000
# Run app.py when the container launches
CMD ["python", "server.py", "run", "--host", "0.0.0.0"]
