"""
Mini expense tracker Agent

A simple project for practicing Tools and ToolContext
"""
from google.adk.tools import ToolContext
from google.adk.agents import Agent



# ============================================
# TOOL 1: Add a expense
# ============================================
def add_expense(amount: float, description: str, category: str, tool_context: ToolContext) -> dict:
    """
    Add a new expense to the tracker.

    Args:
        amount: How much was spent (e.g. 150.50)
        description: What was purchased (e.g. "Groceries at Walmart")
        category: Category of the expense (e.g. "Food", "Transport")
    """
    # Get current list or create a empty one
    expenses = tool_context.state.get("expenses", [])

    new_expense = {
        "id": len(expenses) + 1,
        "amount": amount,
        "description": description,
        "category": category.lower()
    }

    # add and save
    expenses.append(new_expense)
    tool_context.state["expenses"] = expenses

    return {
        "status": "success",
        "message": f"Added ${amount:.2f} for {description} under {category} category.",
        "expense": new_expense
    }

# ============================================
# TOOL 2: Vew expenses
# ============================================
def get_total(tool_context: ToolContext) -> dict:
    """
    Get the total expenses recorded.
    """
    expenses = tool_context.state.get("expenses", [])
    if not expenses:
        return {
            "total": 0.0,
            "count": 0,
            "message": "No expenses yet!."
        }

    total = sum(expense["amount"] for expense in expenses)

    return {
        "total_expenses": round(total, 2),
        "count": len(expenses),
        "message": f"You've spent ${total:.2f} in {len(expenses)} expenses"
    }

# ============================================
# TOOL 3: List all expenses
# ============================================
def list_expenses(tool_context: ToolContext) -> dict:
    """
    List all recorded expenses.

    """
    expenses = tool_context.state.get("expenses", [])
    if not expenses:
        return {"count": 0, "expenses": [], "message": "No expenses recorded"}

    return {
        "count": len(expenses),
        "expenses": expenses,
        "total": round(sum(e["amount"] for e in expenses), 2),
    }

# ============================================
# TOOL 4: View expenses by category
# ============================================
def get_by_category(category: str, tool_context: ToolContext) -> dict:
    """
    Get expenses filtered by category.

    Args:
        category: The category to filter by (e.g. "Food")
    """
    expenses = tool_context.state.get("expenses", [])
    filtered = [e for e in expenses if e["category"] == category.lower()]

    if not filtered:
        return {
            "category": category,
            "count": 0,
            "total": 0,
            "message": f"No expenses in '{category}'"
        }

    total = sum(e["amount"] for e in filtered)

    return {
        "category": category,
        "count": len(filtered),
        "total": round(total, 2),
        "expenses": filtered
    }

# ============================================
# TOOL 5: Delete an expense
# ============================================
def clear_all(tool_context: ToolContext) -> dict:
    """
    Clear all recorded expenses.
    """
    expenses = tool_context.state.get("expenses", [])
    count = len(expenses)

    # clear
    tool_context.state["expenses"] = []

    return {
        "status": "success",
        "deleted": count,
        "message": f"Cleared {count} expenses"
    }

# ============================================
# AGENT DEFINITION
# ============================================
root_agent = Agent(
    name="expense_tracker",
    model="gemini-2.0-flash",
    description="A simple expense tracker to add, view, and manage your expenses.",
    instruction="""You are a friendly expense tracker assistant.

        You help users track their daily expenses. You can:
        - add_expense: Record a new expense with amount, description, and category
        - get_total: Show total spending
        - list_expenses: Show all expenses
        - get_by_category: Filter by category (food, transport, entertainment, etc.)
        - clear_all: Delete all expenses (ask for confirmation first!)

        Common categories: food, transport, entertainment, shopping, bills, health, other

        Always be helpful and format money nicely (e.g., $25.50).
        When showing expenses, organize them clearly.
    """,
    tools=[
        add_expense,
        get_total,
        list_expenses,
        get_by_category,
        clear_all,
    ]
)