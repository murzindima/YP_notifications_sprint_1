FROM python:3.12.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR on
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV POETRY_VERSION 1.7.1

WORKDIR /url_shorter

RUN pip install poetry==$POETRY_VERSION
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-root
COPY . .
RUN chmod +x /url_shorter/init.sh
CMD ["/url_shorter/init.sh"]
