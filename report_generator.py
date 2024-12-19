import csv
import os  # Import nécessaire pour vérifier l'existence des fichiers


def generate_report(input_file, output_file):
    if not os.path.exists(input_file):  # Utilisation de os.path.exists
        print(f"Le fichier {input_file} n'existe pas.")
        return

    total_quantity = 0
    total_value = 0
    category_stats = {}

    with open(input_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Ignorer l'en-tête
        for row in reader:
            name, quantity, unit_price, category = row
            quantity = int(quantity)
            unit_price = float(unit_price)
            total_quantity += quantity
            total_value += quantity * unit_price
            if category not in category_stats:
                category_stats[category] = 0
            category_stats[category] += quantity

    with open(output_file, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Total Quantity"])
        for category, quantity in category_stats.items():
            writer.writerow([category, quantity])
        writer.writerow([])
        writer.writerow(["Total Quantity", total_quantity])
        writer.writerow(["Total Value", round(total_value, 2)])

    print(f"Rapport généré : {output_file}")
