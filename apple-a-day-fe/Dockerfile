# Use the official Node.js image from the Docker Hub
FROM node:latest

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json /app/
RUN npm install

# Copy project files
COPY . /fe/

# Expose port 3000
EXPOSE 3000

# Start the React development server
CMD ["npm", "start"]
