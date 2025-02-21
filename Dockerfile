# Use the latest Python 3.12 slim-bullseye image
FROM python:3.12.9-slim-bullseye

# Install system dependencies required for WeasyPrint
RUN apt-get update -qq \
    && apt-get install -y build-essential python3-dev \
    python3-pip python3-setuptools python3-wheel python3-cffi \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 libffi-dev shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables to optimize Python and pip behavior
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /code

# Copy only the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies and remove the pip cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# (Optional) Specify the command to run your application
# CMD ["python", "your_app.py"]