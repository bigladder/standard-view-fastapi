FROM python:3.13
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG HOST
ARG PORT
ENV HOST=$HOST
ENV PORT=$PORT

ENV PATH="/code/.venv/bin:$PATH"

WORKDIR /code

# Copy from local repo
#COPY . .
# Clone from GitHub
RUN git clone --recurse-submodules --branch main https://github.com/bigladder/standard-view-fastapi.git .

RUN uv sync --all-extras

CMD fastapi run standard_view_fastapi/main.py --host $HOST --port $PORT --no-reload
