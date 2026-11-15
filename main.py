from models import SalesAnalyzer

def main():
    analyzer = SalesAnalyzer("sales.csv")

    if not analyzer.load_data():
        print("Няма данни за анализ. Проверете файла")
        return

    while True:
        print("\n1) Общ приход  2) Приход по категории  3) Филтър по категория")
        print("4) Топ продукти  5) Графика  0) Изход")
        choice = input("Избор: ").strip()

        if choice == "1":
            print(f"Общ приход: {analyzer.total_revenue():.2f} EUR")
        elif choice == "2":
            for category, total in analyzer.revenue_by_category().items():
                print(f"{category}: {total:.2f} EUR")
        elif choice == "3":
            category = input("Категория: ")
            rows = analyzer.filter_by_category(category)
            if not rows:
                print("Няма продажби в тази категория.")
            for row in rows:
                print(row["date"], row["product"], row["quantity"], row["price"])
        elif choice == "4":
            for name, total in analyzer.top_products():
                print(f"{name}: {total:.2f} EUR")
        elif choice == "5":
            analyzer.plot_by_category()
        elif choice == "0":
            break
        else:
            print("Невалиден избор.")


if __name__ == "__main__":
    main()