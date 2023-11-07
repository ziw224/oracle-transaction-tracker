FROM node:latest as build-stage
WORKDIR /app

# Copy the npm config files and install dependencies
COPY package*.json ./
RUN npm install
COPY ./public ./public
COPY ./src ./src

# Build React app
RUN npm run build

# Copy files
FROM python:3.9
WORKDIR /app
COPY main.py .
COPY configure.py .
COPY ./instantclient_zip /app/instantclient_zip/
COPY ./wallet_zip /app/wallet_zip/
COPY ./templates /app/templates/
COPY ./key.txt .
COPY --from=build-stage /app/build ./build

# Install pip dependencies
RUN pip install fastapi uvicorn oracledb jinja2
EXPOSE 8000

CMD ["python3", "main.py"]
