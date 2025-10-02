FROM python:3.11

# WHY: Set working directory inside container
# WHAT: All subsequent commands run from this directory
WORKDIR /app

# WHY: Copy requirements first for better Docker layer caching
# WHAT: If requirements don't change, Docker can reuse this layer
COPY requirements.txt ./

# WHY: Install Python dependencies
# WHAT: pip install reads requirements.txt and installs all packages
RUN pip install --no-cache-dir -r requirements.txt

# WHY: Copy application code
# WHAT: Brings all your Python files into the container
COPY . ./

# WHY: Expose port 8000 for HTTP traffic
# WHAT: Tells Docker this container serves HTTP on port 8000
EXPOSE 8000

# WHY: Define the command to start your application
# WHAT: Runs uvicorn server when container starts
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
