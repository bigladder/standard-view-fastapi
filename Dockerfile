FROM python:3.13
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG PORT
ENV PORT=$PORT

ENV PATH="/code/.venv/bin:$PATH"

WORKDIR /code

#COPY . .
RUN git clone --branch main https://github.com/bigladder/standard-view-fastapi.git .
RUN uv sync --all-extras

CMD fastapi run standard_view_fastapi/main.py --port $PORT
