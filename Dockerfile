# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS /app/service_account_key.json

# Run driveHog.py when the container launches
CMD ["python", "driveHog.py"]
