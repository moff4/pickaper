
FROM python:3.10.3-slim-buster as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry

WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev

FROM python-base as test
RUN poetry install
WORKDIR /app
COPY . .
ENTRYPOINT cicd/entrypoint.sh $0 $@

FROM python-base as prod
WORKDIR /app
COPY pickaper pickaper
ENTRYPOINT cicd/entrypoint.sh $0 $@
CMD ["python", "-m", "pickaper"]
