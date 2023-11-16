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

RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli

# Install pip dependencies
RUN pip install fastapi uvicorn oracledb jinja2 docker

COPY --from=build-stage /app/build ./build

EXPOSE 8000

CMD ["python3", "main.py"]
