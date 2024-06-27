FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1
RUN echo "*****installing dev deps*****"
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev musl-dev libffi-dev \
    && apt-get install -y libmariadb-dev
RUN echo "*****creating app folder*****"
RUN mkdir /app
RUN echo "*****assigning app folder as root folder*****"
WORKDIR /app
RUN echo "*****copy requirements_docker.txt file*****"
COPY requirements.txt /app
RUN echo "*****upgrading pip*****"
RUN python -m pip install --upgrade pip
RUN echo "*****instaliing requirements_docker*****"
RUN pip install --no-deps ruamel.yaml -r requirements.txt
RUN echo "*****copy all files to root app folder*****"
COPY . /app
