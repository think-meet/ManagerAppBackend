# Use official Python image
FROM python:3.12.7

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY manager /app

# Expose the port Django runs on
# EXPOSE 8000

# Run migrations and start Django server
CMD ["sh", "-c", "python manage.py makemigrations core && python manage.py makemigrations && python manage.py migrate && gunicorn manager.wsgi:application --bind 0.0.0.0:8000"]