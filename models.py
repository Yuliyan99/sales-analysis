import csv

import matplotlib.pyplot as plt


class SalesAnalyzer:

    def __init__(self, filename):
        self.filename = filename
        self.records = []

    def load_data(self):
        try:
            with open(self.filename, encoding='utf-8') as file:
                for row in csv.DictReader(file):
                    try:
                        self.records.append({
                            "date": row["date"].strip(),
                            "product": row["product"].strip().title(),
                            "category": row["category"].strip().lower(),
                            "quantity": int(row["quantity"]),
                            "price": float(row["price"]),
                        })
                    except (ValueError, KeyError):
                        print(f"Пропуснат невалиден ред: {row}")
        except FileNotFoundError:
            print(f"Файлът {self.filename} не е намерен.")
            return False
        return bool(self.records)

    def total_revenue(self):
        return sum(r["quantity"] * r["price"] for r in self.records)

    def revenue_by_category(self):
        result = {}
        for record in self.records:
            category = record["category"]
            result[category] = result.get(category, 0) + record["quantity"] * record["price"]
        return result

    def filter_by_category(self, category):
        category = category.strip().lower()
        return [r for r in self.records if r ["category"] == category]

    def top_products(self, n = 3):
        totals = {}
        for record in self.records:
            name = record["product"]
            totals[name] = totals.get(name, 0) + record["quantity"] * record["price"]
        return sorted(totals.items(), key = lambda item: item[1], reverse = True)[:n]

    def plot_by_category(self):
        data = self.revenue_by_category()
        plt.bar(data.keys(), data.values())
        plt.title("Приход по категории")
        plt.ylabel("Приход (EUR)")
        plt.show()