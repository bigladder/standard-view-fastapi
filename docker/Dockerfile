FROM python:3.13
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG PORT=80
ARG SECRET_KEY=6c03627fdc3f3928b5fb04c384ae5c75
ARG CACHE_SIZE=1000
ARG HTTPS_ONLY=False
ARG SESSION_AGE=86400

ENV	PATH="/code/.venv/bin:$PATH" \
		PORT=${PORT} \
		SECRET_KEY=$SECRET_KEY \
		CACHE_SIZE=$CACHE_SIZE \
		HTTPS_ONLY=$HTTPS_ONLY \
		SESSION_AGE=$SESSION_AGE

WORKDIR /code

RUN git clone --branch main https://github.com/bigladder/standard-view-fastapi.git .
RUN uv sync --all-extras

CMD fastapi run standard_view_fastapi/main.py --port $PORT
