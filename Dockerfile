FROM python:3

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN python -m pip install \
        dnspython \
        ppretty \
        tqdm

CMD [ "python" , "ping.py" ]