FROM python:3.13
COPY . /app
EXPOSE 5005
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]