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

print(classify_question("What is my total spending?"))
print(classify_question("What is my largest expense?"))
print(classify_question("What is my average transaction?"))
print(classify_question("How many transactions do I have?"))
print(classify_question("Hello"))