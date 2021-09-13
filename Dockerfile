FROM python:3.8

# ENV http_proxy http://proxy.server:port
# ENV https_proxy http://proxy.server:port
# ENV LC_ALL=C.UTF-8
# ENV LANG=C.UTF-8

WORKDIR /fastapi_app
COPY ./app /fastapi_app/app
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 80
EXPOSE 5566

# if use proxy
# RUN pip install -r requirements.txt --proxy htt://proxy-server....
