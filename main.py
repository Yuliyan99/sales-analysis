from models import SalesAnalyzer

def ask_period(analyzer):
    while True:
        parts = input("Месец (2026-01) или период (2026-01 2026-03), Enter = всички данни: ").split()
        try:
            if not parts:
                analyzer.select_period()
            elif len(parts) <= 2:
                analyzer.select_period(*parts)
            else:
                print("Въведете най-много два месеца.")
                continue
        except ValueError as error:
            print(f"Невалиден период ({error}). Пример: 2026-01 2026-03")
            continue
        break

def main():
    analyzer = SalesAnalyzer("data")

    if not analyzer.load_folder():
        print("Няма данни за анализ. Проверете папката data.")
        return

    ask_period(analyzer)

    while True:
        print(f"\nПериод: {analyzer.period_label}")
        print("1) Общ приход  2) Приход по категории  3) Филтър по категория")
        print("4) Топ продукти  5) Графика  6) Смяна на период 0) Изход")
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
        elif choice == "6":
            ask_period(analyzer)
        elif choice == "0":
            break
        else:
            print("Невалиден избор.")


if __name__ == "__main__":
    main()