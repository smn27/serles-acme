FROM python:3.9
#ADD * /opt/
#ADD ./bin/ /bin/
#ADD ./bin/serles /bin/serles

ENV VIRTUAL_ENV=/opt/serles_venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#RUN . /opt/serles_venv/bin/activate
RUN python3 -m pip install serles-acme

WORKDIR 
COPY ./serles/backends/adcstorest.py /
#WORKDIR /opt
#RUN pip install --upgrade pip && pip install .
#CMD ["python", "pip install ."]
#CMD ["gunicorn", "-b", "0.0.0.0:80", "serles:create_app()"]
#EXPOSE 80

#ENV VIRTUAL_ENV=/opt/venv
#RUN python3 -m venv $VIRTUAL_ENV
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
#COPY requirements.txt .
#RUN pip install -r requirements.txt

# Run the application:
#COPY myapp.py .
#CMD ["python", "myapp.py"]