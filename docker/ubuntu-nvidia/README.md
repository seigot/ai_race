# docker ubuntu-nvidia

run trial

```
xhost local:
docker run -it -e DISPLAY="$DISPLAY" -v /tmp/.X11-unix:/tmp/.X11-unix --gpus 1 --name ai_race_docker seigott/ai_race_docker:ubuntu-nvidia
```

```
docker exec -it ai_race_docker /bin/bash
```

xeyes test

```
apt-get update -y; apt-get install -y x11-apps;
xeyes
```

build

```
docker build -t seigott/ai_race_docker:ubuntu-nvidia .
```

push

```
docker login
docker push seigott/ai_race_docker:ubuntu-nvidia
docker logout
```

