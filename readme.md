# Foodisplay

## 1. 构建镜像

```sh
sudo docker build -t 'foodisplay' .
```

## 2. 运行镜像

```sh
sudo docker run -d -p 4567:4567 --name foodisplay-server foodisplay
```
