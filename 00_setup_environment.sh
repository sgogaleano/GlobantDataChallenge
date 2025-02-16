#!/bin/bash

# Update package list and install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip postgresql postgresql-contrib

# Install required Python packages
pip3 install -r ../requirements.txt

# Start PostgreSQL service
sudo service postgresql start

# Create a PostgreSQL user and database
sudo -u postgres psql -c "CREATE USER testuser WITH PASSWORD 'testpass';"
sudo -u postgres psql -c "CREATE DATABASE globantdb OWNER testuser;"

echo "Environment setup complete."