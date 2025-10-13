# Stage 1: Use an official, lean, and specific Python image as our base.
# Using python:3.11-slim is a good practice for production to keep image size down.
FROM python:3.11-slim

# Set the working directory inside the container. All subsequent commands will run here.
# This directory will be the root for Python's import system.
WORKDIR /app

# Install system-level dependencies required by WeasyPrint.
# This is the reliable, Linux-based way to solve the installation issue.
# --no-install-recommends prevents installing unnecessary optional packages.
# rm -rf /var/lib/apt/lists/* cleans up the package cache to keep the image small.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgobject-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage Docker's layer caching.
# This is a critical optimization: this layer will only be rebuilt if requirements.txt changes.
# The source path 'backend/requirements.txt' is relative to the build context (your project root).
# The destination '.' is relative to the WORKDIR (/app).
COPY backend/requirements.txt .

# Install all Python packages.
# --no-cache-dir is a production best practice to keep the image lean.
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire backend directory from the build context into a 'backend' folder
# inside the container. This creates the /app/backend/ directory structure
# that your absolute imports expect.
COPY backend/ ./backend/

# Document that the application inside the container will listen on port 8000.
EXPOSE 8000

# The command to run your application when the container starts.
# We use the full module path 'backend.main:app' because our WORKDIR is /app.
# We use --host 0.0.0.0 to allow connections from outside the container.
# We do not use --reload in a production Dockerfile.
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]