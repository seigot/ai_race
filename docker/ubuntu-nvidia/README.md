# docker ubuntu-nvidia

## run trial (GUI)

```
xhost local:
docker run -d -e DISPLAY="$DISPLAY" -v /tmp/.X11-unix:/tmp/.X11-unix --gpus 1 --name ai_race_docker seigott/ai_race_docker:ubuntu-nvidia
docker exec -it ai_race_docker /bin/bash
```

### xeyes test

```
apt-get update -y; apt-get install -y x11-apps;
xeyes
```

### nvidia-smi test
```
nvidia-smi
```

## run trial (CUI)

```
docker run -d --gpus 1 --name ai_race_docker_cui seigott/ai_race_docker:ubuntu-nvidia
docker exec -it ai_race_docker_cui /bin/bash
```

### nvidia-smi test
```
nvidia-smi
```

## For developer

### build

```
docker build -t seigott/ai_race_docker:ubuntu-nvidia .
```

### push

```
docker login
docker push seigott/ai_race_docker:ubuntu-nvidia
docker logout
```

