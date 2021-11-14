# pull official base image
FROM python:3.9.6-alpine3.14


# set working directory
RUN mkdir /app
WORKDIR /app

# Turns off buffering for easier container logging
# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1


# install system dependencies
RUN apk update && apk upgrade
RUN apk add --no-cache build-base


# install python dependencies
RUN pip install --upgrade pip
COPY ./app/requirements.txt ./
RUN  pip install --upgrade -r requirements.txt

# add app
COPY ./app .

ENV PORT=8000
EXPOSE 8000

# change app.sh permissions
RUN chmod +x app.sh

CMD ["./app.sh"]


