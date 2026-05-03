# custom-sdl-xapp
This xApp demonstrate GET and SET functions of Redis databases in Near-RT-RIC through the xApps. It use SDL API to access databases and update a key with dummy values in real-time. Author: Pasindu JH. pasindudev2002@gmail.com

## Deploy xApp
Build the Docker image
```bash
docker build -t 127.0.0.1:5000/sdl-xapp:1.0.0 .

```

Push Docker image to local registry

```bash
docker push 127.0.0.1:5000/sdl-xapp:1.0.0
```

Go to descriptor folder and execute following commands.
```bash
sudo CHART_REPO_URL=http://0.0.0.0:8090 dms_cli onboard --config_file_path=config-file.json --shcema_file_path=schema.json
```

Install the xApp within RIC platform.

```bash
sudo CHART_REPO_URL=http://0.0.0.0:8090 dms_cli install sdl-xapp 1.0.0 ricxapp
```
Login to the DBAAS container. Intercept the GET and SET requests to databases using REDIS_CLI MONITOR command.