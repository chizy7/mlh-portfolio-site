#!/bin/bash -x
# MLH PE work

cd /root/mlh-portfolio-site

# Fetch the latest changes from the main branch and reset the local repository
echo "Fetching latest changes from Git..."
git fetch && git reset origin/main --hard
echo "Git fetch and reset complete."

# Spin down containers to prevent out of memory issues
echo "Stopping running Docker containers..."
docker compose -f docker-compose.prod.yml down
echo "Docker containers stopped."

# Build and start the Docker containers
echo "Building and starting Docker containers..."
docker compose -f docker-compose.prod.yml up -d --build
echo "Docker containers are up and running."

echo "Docker Build Complete!"