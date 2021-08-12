# docker build -t eco-device-app -f Dockerfile.test .
# docker run it --rm --name eco-device-app -v ~/eco-devices:/home/eco-devices eco-device-app

# Set base image (host OS)
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY src/ .

# Command to run on container start
CMD [ "python", "app.py" ]