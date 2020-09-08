FROM gcr.io/google_appengine/python

ENV PYTHONUNBUFFERED 1

RUN virtualenv -p python3 /env
ENV PATH /env/bin:$PATH

# Copying & Installing python requirements
ADD requirements.txt /app/requirements.txt
RUN /env/bin/pip install --upgrade pip && /env/bin/pip install -r /app/requirements.txt
ADD . /app

CMD gunicorn -b :8080 backend.wsgi