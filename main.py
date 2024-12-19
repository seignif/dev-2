import csv_handler
import report_generator

def main():
    while True:
        print("\n=== Système de Gestion d'Inventaire ===")
        print("1. Générer des fichiers CSV (données factices)")
        print("2. Consolider les fichiers CSV")
        print("3. Rechercher des informations")
        print("4. Générer un rapport récapitulatif")
        print("5. Quitter")

        choice = input("Choisissez une option : ")
        if choice == "1":
            csv_handler.generate_fake_csv("data/fake_data.csv", 100)
        elif choice == "2":
            consolidated_file = "data/consolidated_inventory.csv"
            csv_handler.consolidate_csv_files(consolidated_file)
        elif choice == "3":
            csv_handler.search_in_csv("data/consolidated_inventory.csv")
        elif choice == "4":
            report_generator.generate_report("data/consolidated_inventory.csv", "data/report.csv")
        elif choice == "5":
            print("Au revoir !")
            break
        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
