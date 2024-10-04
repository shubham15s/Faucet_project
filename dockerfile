# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set environment variables to prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Ensure migrations are run before starting the application
RUN python manage.py migrate --noinput

# Optionally collect static files (for production use)
RUN python manage.py collectstatic --noinput

# The default command to run your Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
