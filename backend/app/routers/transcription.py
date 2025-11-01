"""Transcription endpoints."""

from fastapi import APIRouter, File, UploadFile, Query, HTTPException
from pydantic import BaseModel
from app.services.transcription import TranscriptionService, LanguageDetector
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/transcription", tags=["transcription"])


class TranscriptionResponse(BaseModel):
    """Response for transcription endpoint."""
    text: str
    language: str
    confidence: float


class LanguageDetectionRequest(BaseModel):
    """Request for language detection."""
    text: str


class LanguageDetectionResponse(BaseModel):
    """Response for language detection."""
    language: str
    language_name: str


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = Query(None, description="Language code (e.g., 'en', 'ta'). If not provided, auto-detect."),
) -> TranscriptionResponse:
    """
    Transcribe audio file using Whisper API.

    - **file**: Audio file (webm, mp3, m4a, wav, etc.)
    - **language**: Optional language code (e.g., 'en', 'ta'). If not provided, Whisper will auto-detect.

    Returns transcribed text, detected language, and confidence score.
    """
    try:
        logger.info(f"Received transcription request - file: {file.filename}, language: {language}")

        # Read file content
        audio_content = await file.read()

        if not audio_content:
            raise HTTPException(status_code=400, detail="Empty audio file")

        logger.info(f"Audio file size: {len(audio_content)} bytes")

        if len(audio_content) > 25 * 1024 * 1024:  # 25MB limit from Whisper API
            raise HTTPException(status_code=413, detail="Audio file too large (max 25MB)")

        logger.info("Calling TranscriptionService.transcribe_audio...")

        # Transcribe
        result = await TranscriptionService.transcribe_audio(
            audio_file=audio_content,
            language=language,
            file_name=file.filename or "audio.webm",
        )

        logger.info(f"Transcription successful: {result}")

        return TranscriptionResponse(
            text=result["text"],
            language=result["language"],
            confidence=result["confidence"],
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transcription endpoint error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.post("/detect-language", response_model=LanguageDetectionResponse)
async def detect_language(
    request: LanguageDetectionRequest,
) -> LanguageDetectionResponse:
    """
    Detect language from text.

    Returns language code and full language name.
    """
    try:
        language_code = await LanguageDetector.detect_language(text=request.text)

        # Map language code to name
        language_names = {
            "en": "English",
            "ta": "Tamil",
            "hi": "Hindi",
            "kn": "Kannada",
            "te": "Telugu",
            "ml": "Malayalam",
        }

        language_name = language_names.get(language_code, "Unknown")

        return LanguageDetectionResponse(
            language=language_code,
            language_name=language_name,
        )

    except Exception as e:
        logger.error(f"Language detection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Language detection failed: {str(e)}")
