import unittest
import os
import csv
from inventory_manager.report_generator import generate_report

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        # Fichier CSV d'entrée et sortie pour les tests
        self.input_file = "test_input.csv"
        self.output_file = "test_report.csv"

        # Créer un fichier CSV d'entrée temporaire
        with open(self.input_file, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "quantity", "unit_price", "category"])
            writer.writerow(["Product1", 10, 2.5, "Category1"])
            writer.writerow(["Product2", 5, 3.0, "Category1"])
            writer.writerow(["Product3", 20, 1.5, "Category2"])

    def tearDown(self):
        # Nettoyez les fichiers après chaque test
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_generate_report(self):
        generate_report(self.input_file, self.output_file)
        self.assertTrue(os.path.exists(self.output_file), "Le fichier de rapport n'a pas été généré.")

        # Vérifier le contenu du rapport
        with open(self.output_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)

            # Vérifier les statistiques par catégorie
            self.assertIn(["Category1", "15"], rows, "Les statistiques pour Category1 sont incorrectes.")
            self.assertIn(["Category2", "20"], rows, "Les statistiques pour Category2 sont incorrectes.")

            # Vérifier les totaux
            self.assertIn(["Total Quantity", "35"], rows, "Le total des quantités est incorrect.")
            self.assertIn(["Total Value", "70.0"], rows, "La valeur totale est incorrecte.")  # Corrigé à 70.0 au lieu de 65.0

if __name__ == "__main__":
    unittest.main()
