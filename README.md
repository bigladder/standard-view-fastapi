# Standard View FastAPI

[![Build and Test](https://github.com/bigladder/standard-view-fastapi/actions/workflows/build-and-test.yaml/badge.svg)](https://github.com/bigladder/standard-view-fastapi/actions/workflows/build-and-test.yaml)

## Setup

### UV

From the root `standard-view-fastapi` directory, use [UV] to install dependencies and run [FastAPI] in a virtual environment.
```
uv sync --all-extras
uv run fastapi run standard_view_fastapi\main.py --host=127.0.0.1 --port=80 --no-reload
```

### Docker

From the root `standard-view-fastapi` directory, run `docker-build.bat` or use [Docker] commands to build an image and run [FastAPI] in a container.
```
docker build -t standard_view_fastapi --build-arg HOST=0.0.0.0 --build-arg PORT=80 --progress=plain --no-cache .
docker run -d --name standard_view_fastapi -p 80:80 standard_view_fastapi
```

## References

- [FastAPI]
- [UV]
- [Docker]
- [Python]
- [schema-205]

[FastAPI]: https://fastapi.tiangolo.com/#example
[UV]: https://docs.astral.sh/uv/#installation
[Docker]: https://www.docker.com/products/docker-desktop/
[Python]: https://www.python.org/downloads/
[schema-205]: https://github.com/open205/schema-205/
