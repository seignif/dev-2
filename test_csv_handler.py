import unittest
import os
import csv
from unittest.mock import patch
from io import StringIO
from inventory_manager.csv_handler import  generate_fake_csv, consolidate_csv_files, search_in_csv
import shutil

class TestCSVHandler(unittest.TestCase):

    def setUp(self):
        """Prépare l'environnement de test (nettoyage des fichiers existants)."""
        self.test_dir = "data"
        os.makedirs(self.test_dir, exist_ok=True)

        # Nettoyage des anciens fichiers
        for file in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        self.fake_csv = "data/fake_data.csv"
        self.output_csv = "data/consolidated_data.csv"

    def tearDown(self):
        """Nettoyage après chaque test."""
        if os.path.exists(self.fake_csv):
            os.remove(self.fake_csv)
        if os.path.exists(self.output_csv):
            os.remove(self.output_csv)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)  # Utiliser shutil.rmtree() pour supprimer le répertoire non vide

    def test_generate_fake_csv(self):
        """Test la génération de fichiers CSV avec des données factices."""
        generate_fake_csv(self.fake_csv, 10)

        self.assertTrue(os.path.exists(self.fake_csv), "Le fichier CSV n'a pas été généré.")

        # Vérifier que le fichier contient des en-têtes et des données
        with open(self.fake_csv, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader)
            self.assertEqual(headers, ["name", "quantity", "unit_price", "category"], "Les en-têtes sont incorrects.")

            rows = list(reader)
            self.assertEqual(len(rows), 10, "Le nombre de lignes est incorrect.")

    def test_consolidate_csv_files(self):
        """Test la consolidation de plusieurs fichiers CSV."""
        # Créer quelques fichiers CSV factices dans le dossier 'data'
        for i in range(3):
            generate_fake_csv(f"data/fake_data_{i}.csv", 5)

        consolidate_csv_files(self.output_csv)

        self.assertTrue(os.path.exists(self.output_csv), "Le fichier consolidé n'a pas été créé.")

        # Vérifier que le fichier consolidé contient toutes les lignes des fichiers d'entrée
        with open(self.output_csv, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # ignorer l'en-tête
            rows = list(reader)
            self.assertEqual(len(rows), 15,
                             "Le nombre de lignes consolidées est incorrect.")  # 3 fichiers * 5 lignes par fichier

    @patch('builtins.input', return_value="test")
    @patch('sys.stdout', new_callable=StringIO)
    def test_search_in_csv(self, mock_stdout, mock_input):
        """Test la recherche dans un fichier CSV."""
        # Générer un fichier CSV avec le terme "test"
        with open(self.fake_csv, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "quantity", "unit_price", "category"])
            writer.writerow(["test_product", 10, 2.5, "Category1"])  # Termes contenant "test"
            writer.writerow(["other_product", 5, 3.0, "Category1"])
            writer.writerow(["test_item", 20, 1.5, "Category2"])  # Termes contenant "test"

        # Simuler la recherche d'un terme dans le fichier
        search_in_csv(self.fake_csv)
        output = mock_stdout.getvalue()

        # Vérifier que la recherche a retourné des résultats
        self.assertIn("résultat(s) trouvé(s)", output, "La recherche n'a pas retourné de résultats.")
        self.assertIn("test", output, "Le terme recherché n'a pas été trouvé.")

    def test_search_in_non_existing_file(self):
        """Test la recherche dans un fichier inexistant."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            search_in_csv("non_existing_file.csv")
            output = mock_stdout.getvalue()

            self.assertIn("Le fichier non_existing_file.csv n'existe pas.", output)


if __name__ == "__main__":
    unittest.main()
