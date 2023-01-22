FROM python:3.9

WORKDIR /app
ARG SECRET_KEY
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY=${SECRET_KEY}

COPY pyproject.toml pyproject.toml

# Install dependancies
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Copy project files
COPY src/bug_manager/ .

EXPOSE 8000

CMD poetry run python ./manage.py runserver 0.0.0.0:8000
