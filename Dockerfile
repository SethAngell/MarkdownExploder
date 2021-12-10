FROM python:3.9.5-slim-buster as build

# Set working directory for all following in container commands
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app

# FROM node:12.18.2 as build

# ARG REACT_APP_SERVICES_HOST=/services/m

# WORKDIR /app

# COPY ./package.json /app/package.json
# COPY ./package-lock.json /app/package-lock.json

# RUN yarn install
# COPY . .
# RUN yarn build

# Start with Nginx As our base
FROM nginx:latest

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /usr/src/app /usr/share/nginx/html


