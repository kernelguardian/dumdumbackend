FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ./requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the port
EXPOSE 8080

# # Run the application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
