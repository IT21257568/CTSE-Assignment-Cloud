# Use an official Python image
FROM python:3.13.2-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5003

# Run the application
CMD ["python", "run.py"]
