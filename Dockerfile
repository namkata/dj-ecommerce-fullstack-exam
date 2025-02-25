# Use Python 3.12 as the base image
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ecom.settings.production

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput
## Expose port (Django usually runs on port 8000)
#EXPOSE 8000
#
## Run the application using Gunicorn
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecom.wsgi:application"]
