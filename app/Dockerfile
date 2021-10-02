# pull official base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9


# set working directory
WORKDIR /app
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


# install system dependencies
RUN apt-get update && apt-get clean
    

# install python dependencies
RUN pip install --upgrade pip
COPY ./app/requirements.txt ./
RUN  pip install --no-cache-dir --upgrade -r requirements.txt

# add app
COPY ./app .

ENV PORT=8000
EXPOSE 8000

# change app.sh permissions
RUN chmod +x app.sh

CMD ["./app.sh"]


