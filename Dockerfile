
FROM python:3.10.0
MAINTAINER Mankamal Mishra "mishramankamal1@gmail.com"

COPY . /CollinsAPI
WORKDIR /CollinsAPI
RUN pip3 install -r requirements.txt

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]