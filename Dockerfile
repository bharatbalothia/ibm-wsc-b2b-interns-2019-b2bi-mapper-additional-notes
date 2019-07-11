FROM python:3
MAINTAINER Manjit "smanjit@in.ibm.com"
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -y
RUN apt-get install vim -y
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app_new.py"]
