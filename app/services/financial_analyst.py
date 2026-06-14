from sqlalchemy.orm import Session

from app.services.analytics import get_summary, get_category_breakdown, get_monthly_breakdown


def analyze_question(
    question: str,
    db: Session,
    user_id: int
) -> str:

    question = question.lower()
    summary = get_summary(
            db=db,
            user_id=user_id
        )
    
    month_mapping = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12",
}

    if "total" in question:

        return (
            f"Your total spending is "
            f"{summary.total_spending}"
        )
    
    if "largest expense" in question:

        return (
            f"Your largest expense is "
            f"{summary.largest_expense}"
        )
    
    if "average transaction" in question:

        return (
            f"Your average transaction is "
            f"{summary.average_transaction}"
        )
    
    if "how many" in question and "transaction" in question:

        return (
            f"You have "
            f"{summary.transaction_count} transactions"
        )
    
    if "spend on" in question:
        breakdown = get_category_breakdown(
            db=db,
            user_id=user_id
        )
        for item in breakdown:
            if item.category.lower() in question:
                return (
                    f"You have spent "
                    f"{item.total_spending}  on {item.category}"
                )
        return "I couldn't find that category"
        
    if "spend in" in question:
        breakdown = get_monthly_breakdown(
            db=db,
            user_id=user_id
        )
        for month_name, month_number in month_mapping.items():

            if month_name in question:

                for item in breakdown:

                    if item.month.endswith(month_number):

                        return (
                            f"You spent "
                            f"{item.total_spending} "
                            f"in {month_name.title()}."
                        )

                return (
                    f"No spending data found "
                    f"for {month_name.title()}."
                )

        return (
            "Please specify a month. "
            "For example: 'How much did I spend in January?'"
        )
    
    if "summary" in question:
        return (
            f"Total spending: {summary.total_spending}, "
            f"Transactions: {summary.transaction_count}, "
            f"Average transaction: {summary.average_transaction}, "
            f"Largest expense: {summary.largest_expense}"
        )

    return "I don't understand that question yet."