# Use an official Python base image [cite: 79]
FROM python:3.10-slim

# Set the working directory [cite: 80]
WORKDIR /app

# Copy and install dependencies [cite: 81, 82]
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code [cite: 83]
COPY . .

# Expose the port the app runs on [cite: 84]
EXPOSE 8000

# Run the app [cite: 85]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]