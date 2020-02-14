FROM python:3
ENV PYTHONUNBUFFERED 1
COPY scripts/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY scripts/start.sh /start.sh
RUN chmod +x /start.sh
# COPY . /demo
#RUN chmod +x -R /demo/
EXPOSE 8000
CMD ["/start.sh"]