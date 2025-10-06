# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and Task
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY taskfile.yaml ./
COPY fbar.py ./
COPY test_fbar.py ./

# Install dependencies using uv
RUN uv sync

# Set environment to ensure interactive mode works properly
ENV PYTHONUNBUFFERED=1

# Default command runs the FBAR calculator interactively
CMD ["uv", "run", "python", "fbar.py"]