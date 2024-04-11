# bilivid-metaprocess-server

A server that enhances bilibili video processing with advanced features.

## Features

- Music recognition in videos via ACRCloud API

More features are under development.

## Installation (Docker)

1. Create a directory for the application, e.g., `/opt/bilivid-metaprocess-server`.
2. Clone the repository into the directory: `git clone https://github.com/fred913/bilivid-metaprocess-server.git /opt/bilivid-metaprocess-server/src`.
3. Copy `docker-compose.yml` from the repository to the app directory.
4. Adjust `docker-compose.yml` as needed. For example, modify port mapping or add environment variables.
5. Input your ACRcloud API credentials into the `.env` file (refer to `.env.example` for the format).
6. Launch the application: `docker-compose up -d`.
7. Due to occasional issues causing the application to panic, it's advised to restart the application every minute. Use a shell script (run it every minute via crontab or similar):

```
#!/bin/bash
cd /opt/bilivid-metaprocess-server
docker-compose restart
```

## Usage

The server operates over HTTP and offers the following endpoint:

- `/api/recog_music_in_bili_video`: Accepts three parameters: `video_aid: int, pid: int, target_sec: int`. Returns the same format as the ACRCloud API.

## License
MIT

# To-do

- [ ] STT Provider: OpenAI Whisper API
- [ ] STT Provider: OpenAI Whisper (open-source)
- [ ] STT Provider: other cloud providers'

- [ ] Recognize music from a video using ACRCloud API
- [ ] Speech-to-text recognition from a video using STT 
- [ ] Enhance music recognition by (optinally) removing vocal from the audio signal (by MDX or similar)

- [ ] Pre-built Docker image
