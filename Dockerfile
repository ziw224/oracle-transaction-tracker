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
COPY configure.py .
# Copy instantclient and wallet
COPY ./instantclient_zip /app/instantclient_zip/
COPY ./wallet_zip /app/wallet_zip/
COPY ./key.txt .
COPY --from=build-stage /app/build ./build

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn oracledb
EXPOSE 8000

# Start the FastAPI application with Uvicorn
CMD ["python3", "main.py"]
