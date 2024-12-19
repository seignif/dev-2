import csv
import os
from faker import Faker


def generate_fake_csv(file_name, num_records):
    fake = Faker()
    with open(file_name, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "quantity", "unit_price", "category"])
        for _ in range(num_records):
            writer.writerow([
                fake.word(),
                fake.random_int(min=1, max=100),
                round(fake.random.uniform(1.0, 100.0), 2),
                fake.word()
            ])
    print(f"Fichier généré : {file_name}")


def consolidate_csv_files(output_file):
    files = [f"data/{file}" for file in os.listdir("data") if file.endswith(".csv")]
    if not files:
        print("Aucun fichier CSV trouvé dans le dossier 'data'.")
        return

    with open(output_file, mode="w", newline='', encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(["name", "quantity", "unit_price", "category"])  # En-têtes
        for file in files:
            with open(file, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)  # Ignorer l'en-tête
                writer.writerows(reader)
    print(f"Consolidation terminée : {output_file}")


def search_in_csv(file_name):
    if not os.path.exists(file_name):
        print(f"Le fichier {file_name} n'existe pas.")
        return

    search_term = input("Entrez un terme de recherche (nom ou catégorie) : ").lower()
    with open(file_name, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Ignorer l'en-tête
        results = [row for row in reader if search_term in row[0].lower() or search_term in row[3].lower()]

    if results:
        print(f"{len(results)} résultat(s) trouvé(s) :")
        for result in results:
            print(result)
    else:
        print("Aucun résultat trouvé.")
