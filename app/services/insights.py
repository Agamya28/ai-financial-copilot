from app.services.analytics import (
    get_advanced_analytics
)

def generate_insights(db, user_id):
    analytics = get_advanced_analytics(
        db=db,
        user_id=user_id
    )

    insights = []

    if analytics.top_category:
        insights.append(
            f"Your largest spending category is "
            f"{analytics.top_category.category}."
        )

    if analytics.highest_spending_month:
        insights.append(
            f"Your highest spending month was "
            f"{analytics.highest_spending_month.month}."
        )

    return insights