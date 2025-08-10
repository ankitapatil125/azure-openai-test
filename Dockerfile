# Use official Python slim image as base
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy the requirements file first (for caching)
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files into container
COPY . .

# Set environment variable so Python output is immediate
ENV PYTHONUNBUFFERED=1

# Default command to run your chatbot script (replace chatbot.py with your file)
CMD ["python", "server.py"]
