class Category:
  def __init__(self, category):
      self.category = category
      self.ledger = []

  def deposit(self, amount, description=""):
      self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description=""):
      if self.check_funds(amount):
          self.ledger.append({"amount": -amount, "description": description})
          return True
      return False

  def get_balance(self):
      return sum(item["amount"] for item in self.ledger)

  def transfer(self, amount, budget_category):
      if self.check_funds(amount):
          self.withdraw(amount, f"Transfer to {budget_category.category}")
          budget_category.deposit(amount, f"Transfer from {self.category}")
          return True
      return False

  def check_funds(self, amount):
      return self.get_balance() >= amount

  def __str__(self):
      output = f"{'*' * ((30 - len(self.category)) // 2)}{self.category}{'*' * ((30 - len(self.category)) // 2)}\n"
      for item in self.ledger:
          description = item["description"][:23]
          amount = "{:.2f}".format(item["amount"])
          output += f"{description:<23}{amount:>7}\n"
      output += f"Total: {self.get_balance():.2f}"
      return output


def create_spend_chart(categories):
  total_spent = sum(cat.withdraw(amount=0) for cat in categories)  # Provide a default value for the 'amount' argument

  if total_spent == 0:
    return "No spending data available."

  max_name_length = max(len(cat.category) for cat in categories)
  bars = ["o" * int(round(cat.withdraw(amount=0) / total_spent * 100)) for cat in categories]

  chart = "Percentage spent by category\n"
  for i in range(100, 0, -10):
    chart += f"{i:3d}|"
    for bar in bars:
        chart += f" {'o' if i <= len(bar) * 10 else ' '}  "
    chart += "\n"

  chart += "    ----------\n"

  category_names = [cat.category.ljust(max_name_length) for cat in categories]  # Adjusted for left justification
  for i in range(max_name_length):
    chart += "    "
    for name in category_names:
        chart += f" {name[i] if i < len(name) else ' '}  "
    chart += "\n"

  return chart
