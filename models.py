import csv
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt


class SalesAnalyzer:

    def __init__(self, folder="data"):
        self.folder = folder
        self.records = []
        self.selected = []
        self.period_label = "всички данни"

    def load_data(self, path):
        try:
            with open(path, encoding="utf-8") as file:
                for row in csv.DictReader(file):
                    try:
                        date = row["date"].strip()
                        datetime.strptime(date, "%Y-%m-%d")
                        self.records.append({
                            "date": date,
                            "product": row["product"].strip().title(),
                            "category": row["category"].strip().lower(),
                            "quantity": int(row["quantity"]),
                            "price": float(row["price"]),
                        })
                    except (ValueError, KeyError):
                        print(f"Пропуснат невалиден ред: {Path(path).name}: {row}")
        except FileNotFoundError:
            print(f"Файлът {path} не е намерен.")
            return False
        return True

    def load_folder(self):
        folder = Path(self.folder)
        if not folder.is_dir():
            print(f"Папката '{self.folder}' не е намерена.")
            return False
        files = sorted(folder.glob("*.csv"))
        if not files:
            print(f"В папката '{self.folder}' няма CSV файлове.")
            return False
        for path in files:
            self.load_data(path)
        self.selected = list(self.records)
        return bool(self.records)

    def select_period(self, start=None, end=None):
        if start is None:
            self.selected = list(self.records)
            self.period_label = "всички данни"
            return len(self.selected)
        end = end or start
        try:
            datetime.strptime(start, "%Y-%m")
            datetime.strptime(end, "%Y-%m")
        except ValueError:
            raise ValueError("Грешен формат на месеца.") from None
        if start > end:
            raise ValueError("Началният месец е след крайния.")
        result = [r for r in self.records if start <= r["date"][:7] <= end]
        if not result:
            raise ValueError("Няма продажби за този период.")
        self.selected = result
        self.period_label = start if start == end else f"{start} - {end}"
        return len(self.selected)

    def total_revenue(self):
        return sum(r["quantity"] * r["price"] for r in self.selected)

    def revenue_by_category(self):
        result = {}
        for record in self.selected:
            category = record["category"]
            result[category] = result.get(category, 0) + record["quantity"] * record["price"]
        return result

    def filter_by_category(self, category):
        category = category.strip().lower()
        return [r for r in self.selected if r["category"] == category]

    def top_products(self, n=3):
        totals = {}
        for record in self.selected:
            name = record["product"]
            totals[name] = totals.get(name, 0) + record["quantity"] * record["price"]
        return sorted(totals.items(), key=lambda item: item[1], reverse=True)[:n]

    def plot_by_category(self):
        data = self.revenue_by_category()
        plt.bar(data.keys(), data.values())
        plt.title(f"Приход по категории ({self.period_label})")
        plt.ylabel("Приход (EUR)")
        plt.show()