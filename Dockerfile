FROM python:3.8

RUN apt update
RUN python -m pip install --upgrade pip

WORKDIR /bookstore_project

COPY . /bookstore_project

RUN pip install -r requirements.txt
RUN python3 manage.py migrate

CMD [ "python3", "manage.py", "runserver" ]