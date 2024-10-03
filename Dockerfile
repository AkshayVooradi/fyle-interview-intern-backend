# Use Python 3.7.0 runtime as a base image
FROM python:3.7.0-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the app into the container
COPY . .

# Make the run.sh script executable
RUN chmod +x ./run.sh

# Expose the port Flask/Gunicorn will run on
EXPOSE 7755

# Set the command to run the application using the run.sh script
CMD ["bash", "run.sh"]