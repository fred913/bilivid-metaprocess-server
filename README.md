# bilivid-metaprocess-server

An agent server for processing bilibili video with some advanced features.

## Features

- Recognize music from a video using ACRCloud API

Other features are under development `:-)`

## Installation (Docker)

- Prepare a directory for the application, e.g. `/opt/bilivid-metaprocess-server` (if you want to use a different directory, please modify all the subsequent commands accordingly)
- Clone the repository to the directory: `git clone https://github.com/fred913/bilivid-metaprocess-server.git /opt/bilivid-metaprocess-server/src`
- Take the docker-compose.yml file from the repository and place it in the app directory: `cp /opt/bilivid-metaprocess-server/src/docker-compose.yml /opt/bilivid-metaprocess-server`
- Modify the `docker-compose.yml` file according to your needs, e.g. change the port mapping, or add environment variables.
- Put your ACRcloud API credentials in the `.env` file (check the `.env.example` file for the format)
- Start the application: `docker-compose up -d`
- **Note:** The application currently has some issues, causing it to panic (not providing responses, stuck in a loop, etc.) every few minutes. Since normal responses are given in seconds, it is recommended to restart the application every minute. Here's a shell script for reference (execute it every minute using crontab or similar):

```
#!/bin/bash
cd /opt/bilivid-metaprocess-server  # also, modify this to your app directory
docker-compose restart
```

## Usage

The server works via HTTP, and provides the following endpoint(s):

- `/api/recog_music_in_bili_video`: Takes three parameters: `video_aid: int, pid: int, target_sec: int`
    - Returns the exact same format as what ACRCloud API does, (for reference)[https://docs.acrcloud.cn/metadata/music.html]
