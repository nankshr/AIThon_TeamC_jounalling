"""Task service."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime
from app.models import Task as TaskModel, TaskStatus, TaskPriority
from app.schemas import TaskCreateRequest, TaskUpdateRequest, TaskResponse, TasksListResponse
from typing import List, Optional
import uuid


class TaskService:
    """Service for task operations."""

    @staticmethod
    async def create_task(
        db: AsyncSession,
        user_id: UUID,
        request: TaskCreateRequest,
        entry_id: Optional[UUID] = None,
    ) -> TaskResponse:
        """Create a new task."""
        from datetime import date as dateclass

        task = TaskModel(
            id=uuid.uuid4(),
            user_id=user_id,
            entry_id=entry_id,
            action=request.action,
            description=request.description,
            deadline=dateclass.fromisoformat(request.deadline) if request.deadline else None,
            priority=TaskPriority(request.priority),
            status=TaskStatus.PENDING,
        )

        db.add(task)
        await db.flush()
        await db.refresh(task)

        return _task_to_response(task)

    @staticmethod
    async def get_pending_tasks(
        db: AsyncSession,
        user_id: UUID,
    ) -> TasksListResponse:
        """Get pending tasks for user."""
        stmt = select(TaskModel).where(
            (TaskModel.user_id == user_id) & (TaskModel.status == TaskStatus.PENDING)
        )

        result = await db.execute(stmt)
        tasks = result.scalars().all()

        # Get counts
        completed_stmt = select(func.count(TaskModel.id)).where(
            (TaskModel.user_id == user_id) & (TaskModel.status == TaskStatus.COMPLETED)
        )
        completed_result = await db.execute(completed_stmt)
        completed_count = completed_result.scalar() or 0

        return TasksListResponse(
            total=len(tasks),
            pending_count=len(tasks),
            completed_count=completed_count,
            tasks=[_task_to_response(t) for t in tasks],
        )

    @staticmethod
    async def complete_task(
        db: AsyncSession,
        task_id: UUID,
        user_id: UUID,
    ) -> Optional[TaskResponse]:
        """Mark task as complete."""
        stmt = select(TaskModel).where(
            (TaskModel.id == task_id) & (TaskModel.user_id == user_id)
        )

        result = await db.execute(stmt)
        task = result.scalars().first()

        if not task:
            return None

        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow().isoformat()

        await db.flush()
        await db.refresh(task)

        return _task_to_response(task)

    @staticmethod
    async def update_task(
        db: AsyncSession,
        task_id: UUID,
        user_id: UUID,
        request: TaskUpdateRequest,
    ) -> Optional[TaskResponse]:
        """Update task."""
        from datetime import date as dateclass

        stmt = select(TaskModel).where(
            (TaskModel.id == task_id) & (TaskModel.user_id == user_id)
        )

        result = await db.execute(stmt)
        task = result.scalars().first()

        if not task:
            return None

        if request.action is not None:
            task.action = request.action
        if request.description is not None:
            task.description = request.description
        if request.deadline is not None:
            task.deadline = dateclass.fromisoformat(request.deadline)
        if request.priority is not None:
            task.priority = TaskPriority(request.priority)
        if request.status is not None:
            task.status = TaskStatus(request.status)

        await db.flush()
        await db.refresh(task)

        return _task_to_response(task)

    @staticmethod
    async def get_task_history(
        db: AsyncSession,
        user_id: UUID,
        limit: int = 50,
    ) -> List[TaskResponse]:
        """Get completed task history."""
        stmt = (
            select(TaskModel)
            .where((TaskModel.user_id == user_id) & (TaskModel.status == TaskStatus.COMPLETED))
            .limit(limit)
        )

        result = await db.execute(stmt)
        tasks = result.scalars().all()

        return [_task_to_response(t) for t in tasks]


def _task_to_response(task: TaskModel) -> TaskResponse:
    """Convert Task model to response schema."""
    return TaskResponse(
        id=task.id,
        action=task.action,
        description=task.description,
        deadline=task.deadline.isoformat() if task.deadline else None,
        priority=task.priority.value,
        status=task.status.value,
        completed_at=task.completed_at,
        created_at=task.created_at,
    )
