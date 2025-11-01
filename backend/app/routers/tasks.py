"""Task endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.schemas import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse,
    TasksListResponse,
)
from app.services import TaskService, get_db
from app.services.user import UserService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# For MVP, using a hardcoded user_id
DEFAULT_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


@router.post("", response_model=TaskResponse)
async def create_task(
    request: TaskCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Create a new task."""
    # Ensure user exists
    await UserService.get_or_create_user(db, DEFAULT_USER_ID)
    await db.commit()

    response = await TaskService.create_task(db, DEFAULT_USER_ID, request)
    await db.commit()

    return response


@router.get("/pending", response_model=TasksListResponse)
async def get_pending_tasks(
    db: AsyncSession = Depends(get_db),
) -> TasksListResponse:
    """Get pending tasks for the user."""
    return await TaskService.get_pending_tasks(db, DEFAULT_USER_ID)


@router.get("/history", response_model=list[TaskResponse])
async def get_task_history(
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> list[TaskResponse]:
    """Get completed task history."""
    return await TaskService.get_task_history(db, DEFAULT_USER_ID, limit)


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Mark task as complete."""
    result = await TaskService.complete_task(db, task_id, DEFAULT_USER_ID)

    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.commit()

    return result


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    request: TaskUpdateRequest,
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Update task."""
    result = await TaskService.update_task(db, task_id, DEFAULT_USER_ID, request)

    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.commit()

    return result
