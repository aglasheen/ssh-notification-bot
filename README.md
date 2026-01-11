# SSH Login Monitor

This script monitors the `/var/log/auth.log` file for SSH login events (successful, failed, and invalid user attempts) and sends real-time notifications to a Discord webhook. The script is designed to be run in a Docker container.

## Prerequisites

- Docker
- Docker Compose

## Setup

1.  Create a `.env` file 
2.  Add your Discord webhook URL to the `.env` file:
    ```
    DISCORD_WEBHOOK_URL=https://your-discord-webhook-url
    ```

## Running the script

To run the script, use Docker Compose:

```bash
docker-compose up -d --build
```

This will build the Docker image and run the container in the background. The script will then start monitoring the log file and sending notifications to your Discord webhook.

