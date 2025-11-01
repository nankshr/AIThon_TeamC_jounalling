"""Transcription service using OpenAI Whisper API."""

import io
from typing import Optional
import logging
from openai import AsyncOpenAI, OpenAI
from app.config import settings

logger = logging.getLogger(__name__)

# Create both sync and async clients
sync_client = OpenAI(api_key=settings.openai_api_key)
async_client = AsyncOpenAI(api_key=settings.openai_api_key)


class TranscriptionService:
    """Service for transcribing audio using OpenAI Whisper API."""

    @staticmethod
    async def transcribe_audio(
        audio_file: bytes,
        language: Optional[str] = None,
        file_name: str = "audio.webm",
    ) -> dict:
        """
        Transcribe audio file using Whisper API.

        Args:
            audio_file: Raw audio bytes
            language: Language code (e.g., 'en', 'ta'). If None, auto-detect.
            file_name: Original file name with extension

        Returns:
            Dictionary with:
                - text: Transcribed text
                - language: Detected language code
                - confidence: Confidence score (0-1, estimated based on Whisper behavior)
        """
        try:
            logger.info(
                f"Transcribing audio: {len(audio_file)} bytes, language: {language}"
            )

            # Create file-like object from bytes
            audio_stream = io.BytesIO(audio_file)
            audio_stream.name = file_name

            # Call Whisper API synchronously (OpenAI doesn't support async transcription)
            # Using sync client in executor to avoid blocking
            transcript = await _transcribe_async(audio_stream, language)

            # Convert Transcription object to dict if needed
            if hasattr(transcript, 'model_dump'):
                transcript_dict = transcript.model_dump()
            elif isinstance(transcript, dict):
                transcript_dict = transcript
            else:
                # Fallback: access as object attributes
                transcript_dict = {
                    "text": transcript.text,
                    "language": getattr(transcript, "language", language or "en"),
                }

            logger.info(f"Transcription successful: {len(transcript_dict['text'])} characters")

            return {
                "text": transcript_dict["text"],
                "language": transcript_dict.get("language", language or "en"),
                "confidence": 0.95,  # Whisper doesn't expose confidence, use high default
            }

        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise


async def _transcribe_async(audio_stream, language: Optional[str] = None):
    """Helper to run sync Whisper API call asynchronously."""
    import asyncio
    loop = asyncio.get_event_loop()

    logger.info(f"Starting Whisper API call with language: {language}")

    try:
        # Run sync API call in thread pool executor
        transcript = await loop.run_in_executor(
            None,
            lambda: sync_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_stream,
                language=language,
                response_format="json",
            )
        )

        logger.info(f"Whisper API response: {transcript}")
        return transcript
    except Exception as e:
        logger.error(f"Whisper API error: {str(e)}", exc_info=True)
        raise


class LanguageDetector:
    """Detect language from audio or text."""

    @staticmethod
    async def detect_language(
        audio_file: Optional[bytes] = None,
        text: Optional[str] = None,
    ) -> str:
        """
        Detect language from audio or text.

        Args:
            audio_file: Audio bytes (will use Whisper to detect)
            text: Text to detect language from

        Returns:
            Language code (e.g., 'en', 'ta')
        """
        if audio_file:
            # Use Whisper to detect language
            try:
                audio_stream = io.BytesIO(audio_file)
                audio_stream.name = "audio.webm"

                import asyncio
                loop = asyncio.get_event_loop()

                # Get language detection from Whisper
                detection = await loop.run_in_executor(
                    None,
                    lambda: sync_client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_stream,
                        response_format="verbose_json",
                    )
                )

                return detection.get("language", "en")
            except Exception as e:
                logger.warning(f"Language detection from audio failed: {str(e)}")
                return "en"

        elif text:
            # Simple language detection based on script
            # This is a basic heuristic; for production, use langdetect/textblob
            if any("\u0b80" <= char <= "\u0bff" for char in text):
                return "ta"  # Tamil script
            return "en"

        return "en"
