"""Embeddings service for vector search using OpenAI."""

import logging
from typing import Optional
from openai import AsyncOpenAI
from app.config import settings

logger = logging.getLogger(__name__)

# Initialize async OpenAI client
client = AsyncOpenAI(api_key=settings.openai_api_key)


class EmbeddingsService:
    """Service for generating embeddings using OpenAI."""

    MODEL = "text-embedding-3-small"
    DIMENSIONS = 1536

    @staticmethod
    async def embed_text(text: str) -> list[float]:
        """
        Generate embedding for text.

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding (1536 dimensions)
        """
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for embedding")
                return [0.0] * EmbeddingsService.DIMENSIONS

            logger.info(f"Generating embedding for {len(text)} characters")

            response = await client.embeddings.create(
                model=EmbeddingsService.MODEL,
                input=text,
                dimensions=EmbeddingsService.DIMENSIONS,
            )

            embedding = response.data[0].embedding
            logger.info(f"Generated embedding with {len(embedding)} dimensions")

            return embedding

        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}", exc_info=True)
            raise

    @staticmethod
    async def embed_texts(texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts (batch).

        Args:
            texts: List of texts to embed

        Returns:
            List of embeddings
        """
        try:
            if not texts:
                logger.warning("Empty text list provided for embedding")
                return []

            logger.info(f"Generating embeddings for {len(texts)} texts")

            response = await client.embeddings.create(
                model=EmbeddingsService.MODEL,
                input=texts,
                dimensions=EmbeddingsService.DIMENSIONS,
            )

            embeddings = [item.embedding for item in response.data]
            logger.info(f"Generated {len(embeddings)} embeddings")

            return embeddings

        except Exception as e:
            logger.error(f"Batch embedding generation failed: {str(e)}", exc_info=True)
            raise

    @staticmethod
    async def embed_journal_entries(entries: list[dict]) -> list[dict]:
        """
        Generate embeddings for journal entries.

        Args:
            entries: List of journal entries with 'id' and 'text' keys

        Returns:
            List of entries with 'embedding' added
        """
        try:
            logger.info(f"Embedding {len(entries)} journal entries")

            texts = [entry.get("text", "") for entry in entries]
            embeddings = await EmbeddingsService.embed_texts(texts)

            for entry, embedding in zip(entries, embeddings):
                entry["embedding"] = embedding

            logger.info(f"Successfully embedded {len(entries)} entries")

            return entries

        except Exception as e:
            logger.error(f"Journal entry embedding failed: {str(e)}", exc_info=True)
            raise
