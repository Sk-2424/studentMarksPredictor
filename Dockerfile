# Use official Python 3.9 image as the base image
FROM python:3.9.0 

# Set the working directory in the container
WORKDIR /app

# Copy the entire project in app directory
COPY . /app

# Install dependencies
RUN apt update -y && apt install awscli -y

# Set the default command to run the application
CMD ["python", "app.py"]
