FROM python:3.12-slim

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=2.1.2 POETRY_HOME=/etc/poetry python3 -
ENV PATH="/etc/poetry/bin:$PATH"

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --without test
COPY . .

ENV ENV=production
ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE 8000

CMD [ "sh", "run.sh" ]

