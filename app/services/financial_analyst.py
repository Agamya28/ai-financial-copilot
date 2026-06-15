from sqlalchemy.orm import Session
from app.services.intent_classifier import classify_question
from app.schemas.intent import Intent
from app.services.gemini_service import generate_response
from app.services.analytics import (
    get_summary,
    get_category_breakdown,
    get_monthly_breakdown,
    get_top_category,
    get_lowest_spending_month,
    get_highest_spending_month,
    get_category_percentages
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

        Provide a specific, data-grounded financial insight.
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

        Provide a specific, data-grounded financial insight.
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

        Provide a specific, data-grounded financial insight.
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

        Provide a specific, data-grounded financial insight.
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

                Provide a specific, data-grounded financial insight.
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

                Provide a specific, data-grounded financial insight.
                """

                return generate_response(prompt)

        return (
            f"No spending data found for "
            f"{month_name.title()}."
        )

    if intent_result.intent == Intent.TOP_CATEGORY:

        top_category = get_top_category(
            db=db,
            user_id=user_id
        )

        if not top_category:
            return "No spending data available."

        prompt = f"""
        You are a financial analyst.

        Use only the provided financial data.
        Do not invent numbers.

        User question:
        {question}

        Financial data:
        Top category: {top_category.category}
        Total spending: {top_category.total_spending}

        Provide a specific, data-grounded financial insight.
        """

        return generate_response(prompt)

    if intent_result.intent == Intent.HIGHEST_SPENDING_MONTH:

        month = get_highest_spending_month(
            db=db,
            user_id=user_id
        )

        if not month:
            return "No spending data available."

        prompt = f"""
        You are a financial analyst.

        Use only the provided financial data.
        Do not invent numbers.

        User question:
        {question}

        Financial data:
        Month: {month.month}
        Total spending: {month.total_spending}

        Provide a specific, data-grounded financial insight.
        """

        return generate_response(prompt)

    if intent_result.intent == Intent.LOWEST_SPENDING_MONTH:

        month = get_lowest_spending_month(
            db=db,
            user_id=user_id
        )

        if not month:
            return "No spending data available."

        prompt = f"""
        You are a financial analyst.

        Use only the provided financial data.
        Do not invent numbers.

        User question:
        {question}

        Financial data:
        Month: {month.month}
        Total spending: {month.total_spending}

        Provide a specific, data-grounded financial insight.
        """

        return generate_response(prompt)

    if intent_result.intent == Intent.CATEGORY_PERCENTAGES:

        percentages = get_category_percentages(
            db=db,
            user_id=user_id
        )

        if not percentages:
            return "No spending data available."

        breakdown_text = "\n".join(
            [
                f"{item.category}: {item.percentage}%"
                for item in percentages
            ]
        )

        prompt = f"""
        You are a financial analyst.

        Use only the provided financial data.
        Do not invent numbers.

        User question:
        {question}

        Financial data:
        {breakdown_text}

        Explain the category distribution.
        """

        return generate_response(prompt)


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