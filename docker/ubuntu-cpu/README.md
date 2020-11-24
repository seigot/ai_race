# docker ubuntu-cpu

run trial

```
sudo docker run -p 6081:80 --shm-size=512m seigott/ai_race_docker:ubuntu-cpu
```

build

```
docker build -t seigott/ai_race_docker:ubuntu-cpu .
```

push

```
docker login
docker push seigott/ai_race_docker:ubuntu-cpu
docker logout
```

