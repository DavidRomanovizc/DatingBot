FROM python:3.9.2-alpine3.13

RUN addgroup -S telegrambot && adduser -S telegrambot -G telegrambot

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev postgresql-dev
WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=django_project.telegrambot.telegrambot.settings

USER telegrambot

CMD ["python", "django_app.py", "runserver", "0.0.0.0:8000"]
CMD ["python", "app.py"]
