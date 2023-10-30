FROM python:3.11

COPY . /app/

RUN pip install -r /app/requirements.txt
RUN chmod +x ./app/startup.sh

CMD ["/bin/bash", "-c", "./app/startup.sh"]
