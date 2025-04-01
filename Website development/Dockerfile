# Use an official Node.js runtime as a parent image
FROM node:lts

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install dependencies
RUN npm install

# Expose the port the app runs on
EXPOSE 3000

# Start the application
CMD ["npm", "start"]

