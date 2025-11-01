"""Insight Agent - Recommendations, contradiction detection, and pattern analysis."""

import logging
from typing import Optional
from datetime import datetime, timedelta
from app.services.embeddings import EmbeddingsService

logger = logging.getLogger(__name__)


class InsightAgent:
    """Agent for generating insights from journal entries."""

    @staticmethod
    async def detect_contradictions(entries: list[dict]) -> list[dict]:
        """
        Detect contradictions and conflicts across entries.

        Args:
            entries: List of journal entries with extracted data

        Returns:
            List of detected contradictions with severity levels
        """
        try:
            logger.info(f"Analyzing {len(entries)} entries for contradictions")
            contradictions = []

            # Check budget contradictions
            total_budget = None
            current_spending = 0
            budget_entries = []

            for entry in entries:
                entities = entry.get("entities", {})
                costs = entities.get("costs", [])

                for cost in costs:
                    amount = cost.get("amount", 0)
                    category = cost.get("category", "").lower()

                    if "budget" in category:
                        total_budget = amount
                    else:
                        current_spending += amount
                        budget_entries.append(entry.get("id", "unknown"))

            if total_budget and current_spending > total_budget * 1.2:
                contradictions.append(
                    {
                        "type": "budget_overrun",
                        "severity": "high",
                        "description": f"Budget overrun: Spent ${current_spending:.2f} of ${total_budget:.2f} (${current_spending - total_budget:.2f} over by {((current_spending/total_budget - 1) * 100):.1f}%)",
                        "budget": total_budget,
                        "spent": current_spending,
                        "entries": budget_entries,
                    }
                )
            elif total_budget and current_spending > total_budget:
                contradictions.append(
                    {
                        "type": "budget_concern",
                        "severity": "medium",
                        "description": f"Budget concern: Spent ${current_spending:.2f} of ${total_budget:.2f} (${current_spending - total_budget:.2f} over)",
                        "budget": total_budget,
                        "spent": current_spending,
                        "entries": budget_entries,
                    }
                )

            # Check timeline pressure
            pending_tasks = 0
            days_to_wedding = None
            task_entries = []

            for entry in entries:
                tasks = entry.get("tasks", {})
                explicit_tasks = tasks.get("explicit", [])
                pending = [t for t in explicit_tasks if t.get("status") == "pending"]
                pending_tasks += len(pending)
                if pending:
                    task_entries.append(entry.get("id", "unknown"))

                # Try to find wedding date
                entities = entry.get("entities", {})
                dates = entities.get("dates", [])
                for date_obj in dates:
                    if "wedding" in date_obj.get("event", "").lower():
                        try:
                            wedding_date = datetime.strptime(
                                date_obj.get("date", ""), "%Y-%m-%d"
                            ).date()
                            today = datetime.now().date()
                            days_to_wedding = (wedding_date - today).days
                        except (ValueError, TypeError):
                            pass

            if pending_tasks > 5 and days_to_wedding and days_to_wedding < 30:
                contradictions.append(
                    {
                        "type": "timeline_pressure",
                        "severity": "high",
                        "description": f"Timeline pressure: {pending_tasks} tasks pending with only {days_to_wedding} days to wedding",
                        "pending_tasks": pending_tasks,
                        "days_remaining": days_to_wedding,
                        "entries": task_entries,
                    }
                )
            elif pending_tasks > 10:
                contradictions.append(
                    {
                        "type": "task_overload",
                        "severity": "medium",
                        "description": f"High task load: {pending_tasks} pending tasks to manage",
                        "pending_tasks": pending_tasks,
                        "entries": task_entries,
                    }
                )

            # Check vendor conflicts
            vendors_seen = {}
            vendor_conflicts = []

            for entry in entries:
                entities = entry.get("entities", {})
                vendors = entities.get("vendors", [])

                for vendor in vendors:
                    vendor_name = vendor.get("name", "").lower()
                    vendor_status = vendor.get("status", "").lower()

                    if vendor_name and vendor_name in vendors_seen:
                        if vendor_status == "booked":
                            conflict_info = vendors_seen[vendor_name]
                            vendor_conflicts.append(
                                {
                                    "vendor": vendor.get("name"),
                                    "entries": [conflict_info["entry_id"], entry.get("id")],
                                    "status_1": conflict_info["status"],
                                    "status_2": vendor_status,
                                }
                            )
                    elif vendor_name and vendor_status == "booked":
                        vendors_seen[vendor_name] = {
                            "entry_id": entry.get("id"),
                            "status": vendor_status,
                        }

            if vendor_conflicts:
                contradictions.append(
                    {
                        "type": "vendor_conflict",
                        "severity": "medium",
                        "description": f"Vendor booking conflicts: {len(vendor_conflicts)} vendors with status changes",
                        "conflicts": vendor_conflicts,
                    }
                )

            logger.info(f"Found {len(contradictions)} contradictions")
            return contradictions

        except Exception as e:
            logger.error(f"Contradiction detection failed: {str(e)}", exc_info=True)
            raise

    @staticmethod
    async def generate_insights(entries: list[dict]) -> dict:
        """
        Generate insights from entry patterns and trends.

        Args:
            entries: List of journal entries with metadata

        Returns:
            Dict with various insights and recommendations
        """
        try:
            logger.info(f"Generating insights from {len(entries)} entries")

            insights = {
                "patterns": [],
                "recommendations": [],
                "alerts": [],
                "sentiment_trend": {},
                "budget_status": {},
                "task_summary": {},
            }

            if not entries:
                return insights

            # Analyze sentiment trends
            sentiments = []
            emotions = []

            for entry in entries:
                sentiment = entry.get("sentiment", {})
                if sentiment:
                    emotions.append(sentiment.get("emotion", ""))
                    sentiments.append(sentiment)

            if emotions:
                emotion_counts = {}
                for emotion in emotions:
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

                dominant_emotion = max(emotion_counts, key=emotion_counts.get)
                insights["sentiment_trend"] = {
                    "dominant_emotion": dominant_emotion,
                    "count": emotion_counts[dominant_emotion],
                    "distribution": emotion_counts,
                    "trend_description": f"Recent entries show {dominant_emotion} sentiment (seen {emotion_counts[dominant_emotion]} times)",
                }

                # Generate sentiment-based alerts
                stress_count = emotion_counts.get("stressed", 0) + emotion_counts.get(
                    "anxious", 0
                )
                if stress_count > len(entries) * 0.5:
                    insights["alerts"].append(
                        {
                            "type": "stress_level",
                            "severity": "high",
                            "message": f"Wedding planning stress detected: {stress_count} of {len(entries)} recent entries show stress",
                            "recommendation": "Consider delegating tasks or taking a break",
                        }
                    )

            # Analyze spending patterns
            total_costs = 0
            cost_categories = {}

            for entry in entries:
                entities = entry.get("entities", {})
                costs = entities.get("costs", [])

                for cost in costs:
                    amount = cost.get("amount", 0)
                    category = cost.get("category", "")

                    total_costs += amount
                    cost_categories[category] = cost_categories.get(category, 0) + amount

            if cost_categories:
                largest_category = max(cost_categories, key=cost_categories.get)
                insights["budget_status"] = {
                    "total_spent": total_costs,
                    "by_category": cost_categories,
                    "largest_category": largest_category,
                    "largest_amount": cost_categories[largest_category],
                }

                # Add budget recommendations
                if largest_category:
                    insights["recommendations"].append(
                        {
                            "type": "cost_optimization",
                            "area": largest_category,
                            "amount": cost_categories[largest_category],
                            "message": f"Your largest expense is {largest_category} at ${cost_categories[largest_category]:.2f}. Consider if there are cost-saving options here.",
                        }
                    )

            # Analyze task patterns
            total_tasks = 0
            completed_tasks = 0
            high_priority_tasks = 0

            for entry in entries:
                tasks = entry.get("tasks", {})
                explicit = tasks.get("explicit", [])

                for task in explicit:
                    total_tasks += 1
                    if task.get("status") == "completed":
                        completed_tasks += 1
                    if task.get("priority") == "high":
                        high_priority_tasks += 1

            if total_tasks:
                completion_rate = (completed_tasks / total_tasks) * 100
                insights["task_summary"] = {
                    "total_tasks": total_tasks,
                    "completed": completed_tasks,
                    "pending": total_tasks - completed_tasks,
                    "completion_rate": completion_rate,
                    "high_priority": high_priority_tasks,
                }

                # Task-based recommendations
                if high_priority_tasks > 5:
                    insights["recommendations"].append(
                        {
                            "type": "task_priority",
                            "message": f"You have {high_priority_tasks} high-priority tasks. Focus on these first to avoid last-minute stress.",
                            "count": high_priority_tasks,
                        }
                    )

            # General patterns
            if len(entries) >= 3:
                # Check theme patterns
                all_themes = []
                for entry in entries:
                    themes = entry.get("themes", [])
                    all_themes.extend(themes)

                if all_themes:
                    theme_counts = {}
                    for theme in all_themes:
                        theme_counts[theme] = theme_counts.get(theme, 0) + 1

                    top_themes = sorted(
                        theme_counts.items(), key=lambda x: x[1], reverse=True
                    )[:3]

                    for theme, count in top_themes:
                        insights["patterns"].append(
                            {
                                "type": "recurring_theme",
                                "theme": theme,
                                "frequency": count,
                                "description": f"'{theme}' appears in {count} of your recent entries",
                            }
                        )

            logger.info(
                f"Generated {len(insights['recommendations'])} recommendations and {len(insights['alerts'])} alerts"
            )
            return insights

        except Exception as e:
            logger.error(f"Insight generation failed: {str(e)}", exc_info=True)
            raise

    @staticmethod
    async def get_next_steps(entries: list[dict]) -> list[dict]:
        """
        Generate actionable next steps based on current state.

        Args:
            entries: List of journal entries

        Returns:
            List of recommended next steps with priority
        """
        try:
            logger.info(f"Generating next steps from {len(entries)} entries")

            next_steps = []

            if not entries:
                return next_steps

            # Get the most recent entry for context
            latest_entry = entries[-1] if entries else None

            if latest_entry:
                # Check for pending tasks
                tasks = latest_entry.get("tasks", {})
                explicit_tasks = tasks.get("explicit", [])
                pending = [t for t in explicit_tasks if t.get("status") == "pending"]

                if pending:
                    # Sort by deadline
                    pending.sort(key=lambda x: x.get("deadline", "2099-12-31"))

                    for task in pending[:3]:  # Top 3 pending tasks
                        next_steps.append(
                            {
                                "priority": "high" if task.get("priority") == "high" else "medium",
                                "action": f"Complete: {task.get('title', 'Unknown task')}",
                                "deadline": task.get("deadline"),
                                "reason": f"This task is {task.get('priority', 'medium')}-priority",
                            }
                        )

                # Check for unbooked vendors
                entities = latest_entry.get("entities", {})
                vendors = entities.get("vendors", [])
                unbooked = [v for v in vendors if v.get("status") != "booked"]

                if unbooked:
                    for vendor in unbooked[:2]:  # Top 2 unbooked
                        next_steps.append(
                            {
                                "priority": "high",
                                "action": f"Book vendor: {vendor.get('name', 'Unknown')} ({vendor.get('category', 'unknown')})",
                                "reason": "Vendors should be booked ASAP to secure availability",
                            }
                        )

            # Add general recommendations
            if len(entries) < 4:
                next_steps.append(
                    {
                        "priority": "medium",
                        "action": "Continue journaling regularly",
                        "reason": "More entries help identify trends and provide better insights",
                    }
                )

            # Sort by priority
            priority_order = {"high": 0, "medium": 1, "low": 2}
            next_steps.sort(key=lambda x: priority_order.get(x.get("priority"), 2))

            logger.info(f"Generated {len(next_steps)} next steps")
            return next_steps

        except Exception as e:
            logger.error(f"Next steps generation failed: {str(e)}", exc_info=True)
            raise
