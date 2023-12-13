FROM python:3.9

#set the environment variable for config.ini file in Docker container
ENV CONFIG=/serles-acme/config/config.ini  

WORKDIR  /serles-acme
COPY ./serles/ /serles-acme/serles/
COPY ./requirements.txt /serles-acme/
COPY ./gunicorn_config.py /serles-acme/config/
COPY ./config.ini /serles-acme/config/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#gunicorn wird im WORKDIR folder gestartet, deshalb muss dort der serles Ordner liegen um ihn zu starten
CMD ["gunicorn", "-c", "/serles-acme/config/gunicorn_config.py", "-b", "0.0.0.0:8000", "serles:create_app()"]

EXPOSE 8000