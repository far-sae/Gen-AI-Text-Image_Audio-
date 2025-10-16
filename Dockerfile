# Use lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Make logs print instantly
ENV PYTHONUNBUFFERED=1

# Add /app to Python path so imports like "from src..." work
ENV PYTHONPATH=/app

# Expose Streamlit's default port
EXPOSE 8501

# Command to start your Streamlit app
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
