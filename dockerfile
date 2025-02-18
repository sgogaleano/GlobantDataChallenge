# Use an official Python runtime as a parent image
FROM python:3.12.3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the setup script
RUN chmod +x 00_setup_environment.sh
RUN ./00_setup_environment.sh

# Command to run the FastAPI server
CMD ["uvicorn", "02_apiRest:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]