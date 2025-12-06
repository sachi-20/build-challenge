from dataclasses import dataclass
from datetime import datetime


@dataclass
class SalesRecord:
    """
    Data model representing a single sales transaction with computed properties.
    """
    order_id: str
    customer_name: str
    category: str
    sub_category: str
    city: str
    order_date: datetime
    region: str
    sales: float
    discount: float
    profit: float
    state: str

    @property
    def profit_margin(self) -> float:
        """Calculates and returns the profit margin percentage for the transaction."""
        return (self.profit / self.sales * 100) if self.sales > 0 else 0.0

    @property
    def year(self) -> int:
        """Returns the year extracted from the order date."""
        return self.order_date.year if self.order_date else 0

    @property
    def month(self) -> int:
        """Returns the month extracted from the order date."""
        return self.order_date.month if self.order_date else 0

    @property
    def discount_category(self) -> str:
        """Classifies the discount into Low, Medium, or High."""
        if self.discount < 0.10:
            return "Low"
        elif self.discount < 0.20:
            return "Medium"
        else:
            return "High"
