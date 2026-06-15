from app.schemas.intent import Intent, IntentResult


def classify_question(question: str) -> IntentResult:
    question = question.lower()

    total_keywords = [
        "total spending",
        "total expense",
        "total expenses",
        "spent overall",
        "overall spending",
        "spend in total",
    ]

    largest_keywords = [
        "largest expense",
        "biggest expense",
        "highest expense",
        "largest transaction",
        "largest amount",
        "biggest amount",
    ]

    average_keywords = [
        "average transaction",
        "average expense",
        "average spending",
    ]

    summary_keywords = [
    "summary",
    "overview",
    "spending summary",
    ]

    top_category_keywords = [
    "top category",
    "top spending category",
    "highest spending category",
    "largest category",
    ]

    highest_month_keywords = [
    "highest spending month",
    "month did i spend the most",
    "spent the most",
    "best spending month",
    "highest spending",
    "month had the highest spending",
    "which month had the highest spending",
    ]

    lowest_month_keywords = [
    "lowest spending month",
    "month did i spend the least",
    "spent the least",
    "lowest spending",
    "month had the lowest spending",
    "which month had the lowest spending",
    ]

    category_percentage_keywords = [
    "category percentages",
    "spending percentages",
    "percentage breakdown",
    "category distribution",
    "spending distribution",
    "spending breakdown",
    ]

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

    categories = [
    "food",
    "transport",
    "shopping",
    "entertainment",
    "health",
    ]

    if any(keyword in question for keyword in total_keywords):
        return IntentResult(
            intent=Intent.TOTAL_SPENDING
        )

    if any(keyword in question for keyword in largest_keywords):
        return IntentResult(
            intent=Intent.LARGEST_EXPENSE
        )

    if any(keyword in question for keyword in average_keywords):
        return IntentResult(
            intent=Intent.AVERAGE_TRANSACTION
        )

    if "how many" in question and "transaction" in question:
        return IntentResult(
            intent=Intent.TRANSACTION_COUNT
        )

    if any(keyword in question for keyword in summary_keywords):
        return IntentResult(
            intent=Intent.SPENDING_SUMMARY
        )

    if any(keyword in question for keyword in top_category_keywords):
        return IntentResult(
            intent=Intent.TOP_CATEGORY
        )

    if any(keyword in question for keyword in highest_month_keywords):
        return IntentResult(
            intent=Intent.HIGHEST_SPENDING_MONTH
        )

    if any(keyword in question for keyword in lowest_month_keywords):
        return IntentResult(
            intent=Intent.LOWEST_SPENDING_MONTH
        )

    if any(keyword in question for keyword in category_percentage_keywords):
        return IntentResult(
            intent=Intent.CATEGORY_PERCENTAGES
        )

    for month_name in month_mapping:
        if month_name in question:
            return IntentResult(
                intent=Intent.MONTHLY_SPENDING,
                parameters={
                    "month": month_name
                }
            )
    
    for category in categories:
        if category in question:
            return IntentResult(
                intent=Intent.CATEGORY_SPENDING,
                parameters={
                    "category": category
                }
            )
    
    return IntentResult(
        intent=Intent.UNKNOWN
    )
