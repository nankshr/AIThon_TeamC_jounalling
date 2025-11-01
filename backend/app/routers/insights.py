"""API endpoints for insights and recommendations."""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from app.agents.insight import InsightAgent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["insights"])


class InsightRequest(BaseModel):
    """Request schema for generating insights."""

    entries: list[dict[str, Any]]


class InsightResponse(BaseModel):
    """Response schema for insights."""

    success: bool
    message: str
    insights: Optional[dict[str, Any]] = None
    error: Optional[str] = None


class NextStepsRequest(BaseModel):
    """Request schema for next steps."""

    entries: list[dict[str, Any]]


class NextStepsResponse(BaseModel):
    """Response schema for next steps."""

    success: bool
    message: str
    next_steps: list[dict[str, Any]] = []
    error: Optional[str] = None


class ContradictionsRequest(BaseModel):
    """Request schema for contradiction detection."""

    entries: list[dict[str, Any]]


class ContradictionsResponse(BaseModel):
    """Response schema for contradictions."""

    success: bool
    message: str
    contradictions: list[dict[str, Any]] = []
    count: int = 0
    error: Optional[str] = None


@router.post("/insights", response_model=InsightResponse)
async def generate_insights(request: InsightRequest) -> InsightResponse:
    """
    Generate insights from journal entries.

    This endpoint:
    1. Analyzes patterns in entries
    2. Detects trends (sentiment, spending, tasks)
    3. Generates recommendations
    4. Identifies alerts

    Args:
        request: InsightRequest with list of entries

    Returns:
        Insights with patterns, recommendations, and alerts
    """
    try:
        if not request.entries:
            raise HTTPException(status_code=400, detail="Entries list cannot be empty")

        logger.info(f"Generating insights from {len(request.entries)} entries")

        # Call Insight Agent
        insights = await InsightAgent.generate_insights(request.entries)

        logger.info(
            f"Generated insights: {len(insights.get('recommendations', []))} recommendations, {len(insights.get('alerts', []))} alerts"
        )

        return InsightResponse(
            success=True,
            message="Insights generated successfully",
            insights=insights,
        )

    except HTTPException as e:
        logger.warning(f"HTTP error in insight generation: {e.detail}")
        return InsightResponse(
            success=False,
            message="Invalid request",
            error=str(e.detail),
        )
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}", exc_info=True)
        return InsightResponse(
            success=False,
            message="Insight generation failed",
            error=str(e),
        )


@router.post("/contradictions", response_model=ContradictionsResponse)
async def detect_contradictions(
    request: ContradictionsRequest,
) -> ContradictionsResponse:
    """
    Detect contradictions across journal entries.

    This endpoint detects:
    - Budget overruns (spending >20% over budget)
    - Timeline pressure (<30 days with >5 pending tasks)
    - Vendor conflicts (booking inconsistencies)
    - Task overload (>10 pending tasks)

    Args:
        request: ContradictionsRequest with list of entries

    Returns:
        List of detected contradictions with severity levels
    """
    try:
        if not request.entries:
            raise HTTPException(status_code=400, detail="Entries list cannot be empty")

        logger.info(f"Detecting contradictions in {len(request.entries)} entries")

        # Call Insight Agent
        contradictions = await InsightAgent.detect_contradictions(request.entries)

        logger.info(f"Found {len(contradictions)} contradictions")

        return ContradictionsResponse(
            success=True,
            message="Contradiction detection completed",
            contradictions=contradictions,
            count=len(contradictions),
        )

    except HTTPException as e:
        logger.warning(f"HTTP error in contradiction detection: {e.detail}")
        return ContradictionsResponse(
            success=False,
            message="Invalid request",
            error=str(e.detail),
        )
    except Exception as e:
        logger.error(f"Error detecting contradictions: {str(e)}", exc_info=True)
        return ContradictionsResponse(
            success=False,
            message="Contradiction detection failed",
            error=str(e),
        )


@router.post("/next-steps", response_model=NextStepsResponse)
async def get_next_steps(request: NextStepsRequest) -> NextStepsResponse:
    """
    Generate actionable next steps based on entries.

    This endpoint:
    1. Identifies pending tasks from most recent entry
    2. Recommends high-priority actions
    3. Suggests vendor bookings
    4. Provides deadline-aware recommendations

    Args:
        request: NextStepsRequest with list of entries

    Returns:
        List of recommended next steps with priority levels
    """
    try:
        if not request.entries:
            raise HTTPException(status_code=400, detail="Entries list cannot be empty")

        logger.info(f"Generating next steps from {len(request.entries)} entries")

        # Call Insight Agent
        next_steps = await InsightAgent.get_next_steps(request.entries)

        logger.info(f"Generated {len(next_steps)} next steps")

        return NextStepsResponse(
            success=True,
            message="Next steps generated successfully",
            next_steps=next_steps,
        )

    except HTTPException as e:
        logger.warning(f"HTTP error in next steps generation: {e.detail}")
        return NextStepsResponse(
            success=False,
            message="Invalid request",
            error=str(e.detail),
        )
    except Exception as e:
        logger.error(f"Error generating next steps: {str(e)}", exc_info=True)
        return NextStepsResponse(
            success=False,
            message="Next steps generation failed",
            error=str(e),
        )
