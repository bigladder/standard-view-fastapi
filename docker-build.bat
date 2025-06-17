echo off

set CONTAINER_NAME=standard-view-fastapi
set IMAGE_NAME=standard-view-fastapi
set HOST=0.0.0.0
set PORT=80

docker stop %CONTAINER_NAME%
docker rm %CONTAINER_NAME%
docker rmi %IMAGE_NAME%

docker build -t %IMAGE_NAME% --build-arg HOST=%HOST% --build-arg PORT=%PORT% --progress=plain --no-cache .

docker run -d --name %CONTAINER_NAME% -p %PORT%:%PORT% %IMAGE_NAME%

pause
