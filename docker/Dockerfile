FROM python:3.13
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

RUN git clone --branch main https://github.com/bigladder/standard-view-fastapi.git .
RUN uv sync --all-extras --dev

ENV PATH="/code/.venv/bin:$PATH"

CMD ["fastapi", "run", "standard_view_fastapi/main.py", "--port", "80"]
