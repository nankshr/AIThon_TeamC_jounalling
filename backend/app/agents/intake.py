"""Intake Agent - Entity extraction from journal entries using OpenAI LLM."""

import json
import logging
from typing import Optional, Any
from openai import AsyncOpenAI
from app.config import settings
from app.agents.prompts import INTAKE_AGENT_PROMPT

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=settings.openai_api_key)


class IntakeAgent:
    """Agent for extracting entities and tasks from journal entries using OpenAI GPT-4."""

    @staticmethod
    async def process_entry(
        text: str,
        language: str = "en",
    ) -> dict[str, Any]:
        """
        Process a journal entry and extract entities, tasks, and insights.

        Args:
            text: The journal entry text
            language: Language of the entry (en, ta, hi, etc.)

        Returns:
            Dictionary with extracted entities, tasks, themes, sentiment, etc.
        """
        try:
            logger.info(f"Processing journal entry ({language}): {len(text)} characters")

            # Create the prompt for OpenAI
            user_prompt = f"""Process this journal entry and extract structured information:

Language: {language}

Entry:
{text}

Return valid JSON following the schema provided."""

            # Call OpenAI GPT-4 Turbo
            logger.info("Calling OpenAI GPT-4 for entity extraction")
            response = await client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": INTAKE_AGENT_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,  # Lower temperature for consistency
                max_tokens=2000,
                response_format={"type": "json_object"},  # Ensure JSON response
            )

            # Extract and parse the response
            response_text = response.choices[0].message.content
            logger.info(f"OpenAI response received: {len(response_text)} characters")

            # Parse JSON response
            result = json.loads(response_text)
            logger.info(
                f"Extracted entities - vendors: {len(result.get('entities', {}).get('vendors', []))}, "
                f"tasks: {len(result.get('tasks', {}).get('explicit', []))} explicit + "
                f"{len(result.get('tasks', {}).get('implicit', []))} implicit"
            )

            return {
                "success": True,
                "data": result,
                "model": "gpt-4-turbo-preview",
                "tokens_used": response.usage.total_tokens,
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI JSON response: {str(e)}")
            return {
                "success": False,
                "error": f"Invalid JSON from LLM: {str(e)}",
                "data": None,
            }
        except Exception as e:
            logger.error(f"Intake agent error: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": f"Failed to process entry: {str(e)}",
                "data": None,
            }

    @staticmethod
    async def extract_entities(text: str) -> dict:
        """Extract just entities from text (simplified version)."""
        logger.info("Extracting entities from text")
        result = await IntakeAgent.process_entry(text)

        if result["success"] and result["data"]:
            return result["data"].get("entities", {})
        return {}

    @staticmethod
    async def extract_tasks(text: str) -> dict:
        """Extract just tasks from text (simplified version)."""
        logger.info("Extracting tasks from text")
        result = await IntakeAgent.process_entry(text)

        if result["success"] and result["data"]:
            return result["data"].get("tasks", {"explicit": [], "implicit": []})
        return {"explicit": [], "implicit": []}

    @staticmethod
    async def extract_sentiment(text: str) -> dict:
        """Extract sentiment from text (simplified version)."""
        logger.info("Extracting sentiment from text")
        result = await IntakeAgent.process_entry(text)

        if result["success"] and result["data"]:
            return result["data"].get("sentiment", {"emotion": "neutral", "confidence": 0.5})
        return {"emotion": "neutral", "confidence": 0.0}
