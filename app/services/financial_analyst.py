from sqlalchemy.orm import Session
from app.services.intent_classifier import classify_question
from app.schemas.intent import Intent
from app.services.gemini_service import generate_response
from app.services.analytics import (
    get_summary,
    get_category_breakdown,
    get_monthly_breakdown
)


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
    intent_result = classify_question(question)

    if intent_result.intent == Intent.TOTAL_SPENDING:

        prompt = f"""
        You are a financial analyst.

        Use only the provided financial data.
        Do not invent numbers.

        User question:
        {question}

        Financial data:
        Total spending: {summary.total_spending}

        Give a short, professional answer.
        """

        return generate_response(prompt)

    if intent_result.intent == Intent.LARGEST_EXPENSE:

        prompt = f"""
        You are a financial analyst.

        Use only the provided financial data.
        Do not invent numbers.

        User question:
        {question}

        Financial data:
        Largest expense: {summary.largest_expense}

        Give a short, professional answer.
        """

        return generate_response(prompt)

    if intent_result.intent == Intent.AVERAGE_TRANSACTION:

        prompt = f"""
        You are a financial analyst.

        Use only the provided financial data.
        Do not invent numbers.

        User question:
        {question}

        Financial data:
        Average transaction: {summary.average_transaction}

        Give a short, professional answer.
        """

        return generate_response(prompt)

    if intent_result.intent == Intent.TRANSACTION_COUNT:

        prompt = f"""
        You are a financial analyst.

        Use only the provided financial data.
        Do not invent numbers.

        User question:
        {question}

        Financial data:
        Transaction count: {summary.transaction_count}

        Give a short, professional answer.
        """

        return generate_response(prompt)

    if intent_result.intent == Intent.CATEGORY_SPENDING:

        breakdown = get_category_breakdown(
            db=db,
            user_id=user_id
        )
        category = intent_result.parameters.get("category")
        for item in breakdown:

            if item.category.lower() == category:

                prompt = f"""
                You are a financial analyst.

                Use only the provided financial data.
                Do not invent numbers.

                User question:
                {question}

                Financial data:
                Category: {item.category}
                Total spending: {item.total_spending}

                Give a short, professional answer.
                """

                return generate_response(prompt)

        return "I couldn't find that category."

    if intent_result.intent == Intent.MONTHLY_SPENDING:

        breakdown = get_monthly_breakdown(
            db=db,
            user_id=user_id
        )

        month_name = intent_result.parameters.get("month")
        month_number = month_mapping[month_name]

        for item in breakdown:

            if item.month.endswith(month_number):

                prompt = f"""
                You are a financial analyst.

                Use only the provided financial data.
                Do not invent numbers.

                User question:
                {question}

                Financial data:
                Month: {month_name.title()}
                Total spending: {item.total_spending}

                Give a short, professional answer.
                """

                return generate_response(prompt)

        return (
            f"No spending data found for "
            f"{month_name.title()}."
        )

    if intent_result.intent == Intent.SPENDING_SUMMARY:

        prompt = f"""
        You are a financial analyst.

        Use only the provided financial data.
        Do not invent numbers.

        User question:
        {question}

        Financial data:
        Total spending: {summary.total_spending}
        Transaction count: {summary.transaction_count}
        Average transaction: {summary.average_transaction}
        Largest expense: {summary.largest_expense}

        Give a concise spending summary with key insights.
        """

        return generate_response(prompt)

    return "I don't understand that question yet."