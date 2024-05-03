# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

################################################################################

# The example below uses the PHP Apache image as the foundation for running the app.
# By specifying the "apache" tag, it will also use whatever happens to be the
# most recent version of that tag when you build your Dockerfile.
# If reproducability is important, consider using a specific digest SHA, like
# php@sha256:99cede493dfd88720b610eb8077c8688d3cca50003d76d1d539b0efc8cca72b4.
FROM php:8.2-fpm as npontuweb

#install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends libzip-dev libonig-dev && rm -rf /var/lib/apt/lists/*

#install php extensions
RUN docker-php-ext-install pdo_mysql zip mbstring exif pcntl

# Install additional php extension oniguruma
RUN apt-get update && apt-get install -y --no-install-recommends libonig5 && rm -rf /var/lib/apt/lists/*

#clear up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy app files from the app directory.
COPY ./src /var/www/html

#Set working directory
WORKDIR /var/www/html

#Expose port 4000 and start php-fpm server
EXPOSE 4000
CMD [ "php-fpm" ]