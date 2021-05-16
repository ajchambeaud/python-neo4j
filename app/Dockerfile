FROM python:3 as base

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM base as test  
CMD [ "pytest" ]

FROM base as prod
CMD [ "flask", "run", "--host=0.0.0.0"]
