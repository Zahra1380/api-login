# Use the official Python image as the base
FROM python:3.12.0

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY app/requirments.txt requirments.txt
RUN pip install --no-cache-dir -r  requirments.txt

# Copy the project code into the container
COPY app/ .
# Expose the port your FastAPI app will run on
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
