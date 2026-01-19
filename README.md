![Eavesdrop](/assets/eavesdrop_readme.png)

![Python](https://img.shields.io/badge/Python-3-blue?logo=python&logoColor=white)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ethanc/eavesdrop/workflow.yaml)
![Docker Pulls](https://img.shields.io/docker/pulls/ethanchrisp/eavesdrop?label=Docker%20Pulls)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/ethanchrisp/eavesdrop/latest?label=Docker%20Image%20Size)

# Eavesdrop

Eavesdrop is a Discord Bot that transcribes voice messages and media attachments. It is powered by the [whisper.cpp](https://github.com/ggml-org/whisper.cpp) speech-to-text engine.

## Getting Started

> [!IMPORTANT]
> - [Discord API](https://discord.com/developers/) credentials for a Bot user are required.
> - [whisper.cpp](https://github.com/ggml-org/whisper.cpp) server must be accessible via HTTP.
> - [ffmpeg](https://github.com/FFmpeg/FFmpeg) must be installed and accessible via the system PATH.

### Quick Start: Docker (Recommended)

Edit and run this `compose.yaml` example with `docker compose up -d`.

```yaml
services:
  eavesdrop:
    container_name: eavesdrop
    image: ethanchrisp/eavesdrop:latest
    environment:
      LOG_LEVEL: INFO
      LOG_DISCORD_WEBHOOK_URL: https://discord.com/api/webhooks/XXXXXXXX/XXXXXXXX
      LOG_DISCORD_WEBHOOK_LEVEL: WARNING
      DISCORD_BOT_TOKEN: XXXXXXXX
      DISCORD_SERVER_IDS: 0000000000
      WHISPER_API_BASE_URL: http://localhost:1234
    restart: unless-stopped
```

### Standalone

> [!NOTE]
> Eavesdrop targets Python 3.14 and newer. Compatibility with earlier versions is not guaranteed.

Install Python and the required dependencies with [uv](https://github.com/astral-sh/uv):

```
uv sync
```

Rename `.env.example` to `.env` and configure your environment.

Run Eavesdrop with uv.

```
uv run eavesdrop.py -OO
```

### Configuration

All configuration is managed through environment variables on the system hosting the Bot instance.

| **Environment Variable**          | **Description**                                                                                                                         | **Default**           |
|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| `LOG_LEVEL`                       | [Loguru level](https://loguru.readthedocs.io/en/stable/api/logger.html#levels) of log events to print to the console.                   | `INFO`                |
| `LOG_DISCORD_WEBHOOK_URL`         | Discord Webhook URL to forward log events to.                                                                                           | N/A                   |
| `LOG_DISCORD_WEBHOOK_LEVEL`       | [Loguru level](https://loguru.readthedocs.io/en/stable/api/logger.html#levels) of log events to forward to Discord.                     | N/A                   |
| `DISCORD_BOT_TOKEN` (Required)    | [Discord API](https://discord.com/developers/docs/quick-start/getting-started#fetching-your-credentials) credentials for your Bot user. | N/A                   |
| `DISCORD_SERVER_IDS` (Required)   | Comma-separated list of Discord server IDs to sync commands to.                                                                         | N/A                   |
| `WHISPER_API_BASE_URL` (Required) | Base URL for the [whisper.cpp](https://github.com/ggml-org/whisper.cpp) API server.                                                     | N/A                   |

## Disclaimer

Eavesdrop is not affiliated with or endorsed by Activision or Discord.

All trademarks and assets belong to their respective owners.
