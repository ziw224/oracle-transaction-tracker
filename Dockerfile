FROM node:latest as build-stage
WORKDIR /app

# Copy the npm config files and install dependencies
COPY package*.json ./
RUN npm install
COPY ./public ./public
COPY ./src ./src

# Build React app
RUN npm run build

# Set up FastAPI & copy react build
FROM python:3.9
WORKDIR /app
COPY main.py .
COPY --from=build-stage /app/build ./build

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn
EXPOSE 8000

# Start the FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
