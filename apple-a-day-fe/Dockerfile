# Use the official Node.js image from the Docker Hub
FROM node:latest

# Copy project files
COPY . /fe

# Set working directory
WORKDIR /fe

# Install dependencies
RUN npm install

# Expose port 3000
EXPOSE 3000

# Start the React development server
CMD ["npm", "start"]
