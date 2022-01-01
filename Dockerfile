FROM python:3.9.5-slim-buster as build

ARG loki_user
ARG loki_pass
ENV loki_user ${loki_user}
ENV loki_pass ${loki_pass}

# Install Libraries
RUN apt-get update \
  && apt-get -y install pandoc texlive-latex-extra nano\
  && apt-get clean

# Set working directory for all following in container commands
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG True

# Install requirements
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

# Grab files
COPY ./app /usr/src/app

# Compile content
RUN python MarkdownExploder.py

# Start with Nginx As our base
FROM nginx:latest

COPY ./app/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /usr/src/app /usr/share/nginx/html


