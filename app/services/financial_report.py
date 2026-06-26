from sqlalchemy.orm import Session
from app.services.financial_context import build_financial_context
from app.services.gemini_service import generate_response

def generate_financial_report(
    db: Session,
    user_id: int
):
    context = build_financial_context(
    db=db,
    user_id=user_id
)
    prompt = f"""
    You are an expert personal finance advisor.
    
    Generate a comprehensive financial health report.

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

    Generate the report in VALID MARKDOWN format.

    Use the following structure exactly:

    # Financial Health Report

    ## Overall Financial Health

    ## Key Findings

    ## Spending Patterns

    ## Budget Analysis

    ## Savings Opportunities

    ## Personalized Recommendations

    Formatting rules:
    - Use Bold headings (# and ##).
    - Use bullet points where appropriate.
    - Bold important numbers and categories.
    - Use only the provided financial data.
    - Do not invent numbers.

    Keep report under 400 words.
    Use Indian Rupees (₹).
    """

    try:
        return generate_response(prompt)
    except Exception:
        return (
            "Unable to generate report at the moment. "
            "Please try again later."
        )