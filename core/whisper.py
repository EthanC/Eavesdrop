"""Module for interacting with whisper.cpp."""

from typing import Any

import ffmpeg
import niquests
from loguru import logger
from niquests import Response

from core.consts import WHISPER_API_BASE_URL


async def inference(
    audio_url: str, audio_name: str, audio_type: str | None
) -> str | None:
    """Return a text transcription of the audio from the provided URL."""
    # Timeout is 900s (15m) inline with time token is valid
    # https://docs.discord.com/developers/interactions/receiving-and-responding#followup-messages
    res_audio: Response = await niquests.aget(audio_url, timeout=900, stream=True)

    logger.debug(f"HTTP {res_audio.status_code} GET {res_audio.url}")

    audio_data: bytes | None = await res_audio.content

    logger.trace(f"{audio_data=}")

    if not audio_data:
        raise RuntimeError("Failed to download audio content")

    if audio_type != "audio/wav":
        audio_data = await to_wav(audio_data)

    # Timeout is 900s (15m) inline with time token is valid
    # https://docs.discord.com/developers/interactions/receiving-and-responding#followup-messages
    res_transcript: Response = await niquests.apost(
        f"{WHISPER_API_BASE_URL}/inference",
        data={
            "temperature": "0.0",
            "temperature_inc": "0.2",
            "response_format": "json",
        },
        files={"file": (audio_name, audio_data)},
        timeout=900,
    )

    logger.debug(f"HTTP {res_transcript.status_code} GET {res_transcript.url}")
    logger.trace(f"{res_transcript.text=}")

    data: dict[str, Any] = res_transcript.json()

    if error := data.get("error"):
        raise RuntimeError(f"Whisper failed to transcribe audio: {error}")

    text: str | None = data.get("text")

    if not text:
        raise RuntimeError("Whisper returned no transcription text")

    result: str = ""

    for line in text.splitlines():
        result += f"> {line.strip()}\n"

    result = result.strip()

    logger.info(f"Transcribed audio {audio_name}: {result}")

    return result


async def to_wav(in_bytes: bytes) -> bytes:
    """Return the provided audio bytes as WAV format."""
    process = (
        ffmpeg.input("pipe:0")
        .output("pipe:1", format="wav")
        .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
    )
    wav, stderr = process.communicate(input=in_bytes)

    if process.returncode != 0:
        raise RuntimeError(f"ffmpeg failed to convert to WAV: {stderr.decode()}")

    logger.debug("Converted input to WAV audio")

    return wav
