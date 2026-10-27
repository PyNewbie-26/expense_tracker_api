from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class Expense:
    def __init__(self, item: str, amount: float, category: str):
        self.item = item
        self.amount = amount
        self.category = category

    def __str__(self):
        return f"{self.item} {self.amount} {self.category}"

    def to_dict(self):
        return {"item": self.item, "amount": self.amount, "category": self.category}


class ExpenseTracker:
    def __init__(self):
        self.balance = 212000
        self.expenses = []

    def add_expense(self, item: str, amount: float, category: str):
        if amount > self.balance:
            print("You don't have enough money")
            return False
        else:
            self.balance -= amount
            self.expenses.append(Expense(item, amount, category))
            print("Expense added")
            return True

    def get_balance(self):
        return self.balance

    def show_all_expenses(self):
        if len(self.expenses) <= 0:
            print("No expenses to show")
            return
        print("Expenses:")
        total = 0
        for i in range(len(self.expenses)):
            exp = self.expenses[i]
            print(f"{i+1}. {exp.item} - {exp.amount} [{exp.category}] ")
            total += exp.amount
        print(f"{total} ")

    def delete_expenses(self, index_to_delete: int):
        if index_to_delete < 1 or index_to_delete > len(self.expenses):
            print("No expenses to delete")
            return False

        target_index = index_to_delete - 1
        removed_expense = self.expenses.pop(target_index)
        self.balance += removed_expense.amount

        print("Expenses deleted")
        return True


# ============ FASTAPI ============
app = FastAPI()
tracker = ExpenseTracker()


@app.get("/balance")
def get_balance():
    return {"balance": tracker.get_balance()}


class ExpenseIn(BaseModel):
    item: str
    amount: float = Field(..., gt=0)
    category: str

@app.post("/expense", status_code=201)
def add_expense(expense: ExpenseIn):
    added = tracker.add_expense(expense.item, expense.amount, expense.category)
    if not added:
        raise HTTPException(status_code=400, detail="Not enough money")
    return tracker.expenses[-1].to_dict()

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    if expense_id < 1 or expense_id > len(tracker.expenses):
        raise HTTPException(status_code=404, detail="Expense not found")
    return tracker.expenses[expense_id - 1].to_dict()

@app.get("/expenses")
def get_expenses():
    return {
        position: expense.to_dict()
        for position, expense in enumerate(tracker.expenses, start=1)
    }

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    deleted = tracker.delete_expenses(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"Success": "Expense deleted"}

@app.get("/total_expenses")
def get_total_expenses():
    total = 0
    for expense in tracker.expenses:
        total += expense.amount
    return {"Total": total}