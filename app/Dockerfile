# pull official base image
FROM python:3.9.2

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean

# install python dependencies
RUN pip install --upgrade pip

COPY ./app/requirements.txt .
RUN  pip install --no-cache-dir -r requirements.txt

COPY ./app /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 8000
# change script permissions and run
RUN chmod +x ./app_reload.sh
CMD ["./app_reload.sh"]


