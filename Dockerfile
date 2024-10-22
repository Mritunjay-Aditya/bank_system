FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt file
COPY requirements.txt .

# Install the dependencies and upgrade pip to avoid potential issues
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . .

# Expose the necessary port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
