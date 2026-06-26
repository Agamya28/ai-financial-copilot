from sqlalchemy.orm import Session
from app.services.intent_classifier import classify_question
from app.schemas.intent import Intent
from app.services.gemini_service import generate_response
from app.services.budget import get_budget_status
from app.services.financial_context import build_financial_context
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
    BASE_PROMPT = """
        You are a financial analyst.

        Use only the provided financial data.
        Do not invent numbers.
        Do not use markdown formatting.
        Respond in plain text.
        Use Indian Rupees (₹) when referring to money.
        """
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
        {BASE_PROMPT}

        User question:
        {question}

        Financial data:
        Total spending: {summary.total_spending}

        Provide a specific, data-grounded financial insight.
        """

        return generate_response(prompt)

    if intent_result.intent == Intent.LARGEST_EXPENSE:

        prompt = f"""
        {BASE_PROMPT}

        User question:
        {question}

        Financial data:
        Largest Expense: {summary.largest_expense}

        Provide a specific, data-grounded financial insight.
        """

        return generate_response(prompt)

    if intent_result.intent == Intent.AVERAGE_TRANSACTION:

        prompt = f"""
        {BASE_PROMPT}

        User question:
        {question}

        Financial data:
        Average Transaction: {summary.average_transaction:.2f}

        Provide a specific, data-grounded financial insight.
        """

        return generate_response(prompt)

    if intent_result.intent == Intent.TRANSACTION_COUNT:

        prompt = f"""
        {BASE_PROMPT}

        User question:
        {question}

        Financial data:
        Number of Transactions: {summary.transaction_count}

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
                {BASE_PROMPT}

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
                {BASE_PROMPT}

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
        {BASE_PROMPT}

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
        {BASE_PROMPT}

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
        {BASE_PROMPT}

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
        {BASE_PROMPT}

        User question:
        {question}

        Financial data:
        {breakdown_text}

        Provide a specific, data-grounded financial insight.
        """

        return generate_response(prompt)


    if intent_result.intent == Intent.SPENDING_SUMMARY:

        prompt = f"""
        {BASE_PROMPT}

        User question:
        {question}

        Financial data:
        Total spending: {summary.total_spending}
        Transaction count: {summary.transaction_count}
        Average transaction: {summary.average_transaction}
        Largest expense: {summary.largest_expense}

        Provide a specific, data-grounded financial insight.
        """

        return generate_response(prompt)
    
    if intent_result.intent == Intent.BUDGET_ANALYSIS:

        budgets = get_budget_status(
            db=db,
            user_id=user_id
        )

        if not budgets:
            return (
                "You haven't created any budgets yet."
            )

        budget_text = "\n\n".join(
                    [
                        f"""
            Category: {item.category}
            Budget: ₹{item.monthly_limit}
            Spent: ₹{item.spent}
            Remaining: ₹{item.remaining}
            Usage: {item.percentage_used}%
            Status: {
                "OVER_BUDGET"
                if item.spent > item.monthly_limit
                else "WITHIN_BUDGET"
            }
            """
                        for item in budgets
                    ]
                )

        prompt = f"""
        {BASE_PROMPT}

        User question:
        {question}

        Budget Analysis Data:
        {budget_text}

        Provide a specific, data-grounded financial insight.
        """

        return generate_response(prompt)


    context = build_financial_context(
        db=db,
        user_id=user_id
    )

    prompt = f"""
    {BASE_PROMPT}

    You are an expert personal finance advisor.

    Analyze the user's complete financial profile and answer their question.

    Financial Summary:
    {context['summary']}

    Category Breakdown:
    {context['category_breakdown']}

    Monthly Spending:
    {context['monthly_spending']}

    Budget Status:
    {context['budget_status']}

    Insights:
    {context['insights']}

    User Question:
    {question}

    Instructions:
    - Use ONLY the provided financial data.
    - Mention specific numbers whenever possible.
    - Give personalized recommendations.
    - Suggest concrete actions the user can take.
    - Keep the response concise (under 250 words).
    - Use Indian Rupees (₹).
    """

    return generate_response(prompt)