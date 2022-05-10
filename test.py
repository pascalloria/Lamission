import json
import os.path
import unittest
from unittest.mock import patch
import questionnaire

import questionnaire_import


def additionner(a, b):
    return a + b


def conv_nombre():
    num_str = input("Rentrer un nombre: ")
    return int(num_str)


"""class TestUnitaireDemo(unittest.TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_additionner1(self):
        self.assertEqual(additionner(5, 10), 15)

    def test_additionner2(self):
        self.assertEqual(additionner(6, 10), 16)

    def test_conversion_nombre_valide(self):
        with patch("builtins.input", return_value="10"):
            self.assertEqual(conv_nombre(), 10)
        with patch("builtins.input", return_value="100"):
            self.assertEqual(conv_nombre(), 100)

    def test_conversion_nombre_invalide(self):
        with patch("builtins.input", return_value="abcd"):
            self.assertRaises(ValueError, conv_nombre)"""


class TestQuestion(unittest.TestCase):
    def test_question_bonne_mauvaise_reponse(self):
        choix = ("choix1", "choix2", "choix3")
        q = questionnaire.Question("Titre_question", choix, "choix2", 1, 1)
        with patch("builtins.input", return_value="1"):
            self.assertFalse(q.poser())
        with patch("builtins.input", return_value="2"):
            self.assertTrue(q.poser())
        with patch("builtins.input", return_value="3"):
            self.assertFalse(q.poser())


class TestQuestionnaire(unittest.TestCase):
    def test_questionnaire_lancer_alien_debutant(self):
        filename=os.path.join("test_data","cinema_alien_expert.json")
        q=questionnaire.fromData(filename)
        self.assertIsNotNone(q)
        #questionnaire.Questionnaire(q).lancer()
        #nb de questions
        self.assertEqual(len(q[0]),30)
        # titre
        self.assertEqual(q[1]['titre'],"Alien")
        # categorie,
        self.assertEqual(q[1]['categorie'], "Cin\u00e9ma")
        # difficulté
        self.assertEqual(q[1]['difficulte'], "expert")
        # score si l'utilisateur repond "1" a chaque fois
        with patch("builtins.input",return_value="1"):
            self.assertEqual(questionnaire.Questionnaire(q[0]).lancer(),9)

    def test_format_invalide(self):
        filename = os.path.join("test_data", "cinema_alien_expert_invalide.json")
        q = questionnaire.fromData(filename)
        self.assertIsNotNone(q)
        self.assertEqual(q[1]['categorie'], "inconnue")
        self.assertEqual(q[1]['difficulte'], "inconnue")
        self.assertIsNotNone(q[0])

        filename = os.path.join("test_data", "cinema_alien_expert_invalide_v2.json")
        q = questionnaire.fromData(filename)
        self.assertIsNone(q)

        filename = os.path.join("test_data", "cinema_alien_expert_invalide_v3.json")
        q = questionnaire.fromData(filename)
        self.assertIsNone(q)

class TestImportQuestionnaire(unittest.TestCase):
    def test_import_format_json(self):
        questionnaire_import.generate_json_file("Animaux", "Les chats", "https://www.kiwime.com/oqdb/files/1050634995/OpenQuizzDB_050/openquizzdb_50.json")

        filenames=("animaux_leschats_confirme.json","animaux_leschats_debutant.json","animaux_leschats_expert.json")

        for filename in filenames:
            self.assertTrue(os.path.isfile(filename))
            file=open(filename,"r")
            json_data=file.read()
            file.close()
            try:
                data=json.loads(json_data)
            except:
                self.fail(f"Probleme de désérialisation pour le fichier{filename}")
            # titre
            self.assertIsNotNone(data.get("titre"))
            # questions
            self.assertIsNotNone(data.get("questions"))
            # difficulté,
            self.assertIsNotNone(data.get("difficulte"))
            # categorie
            self.assertIsNotNone(data.get("categorie"))
            # questions >
            for question in data["questions"]:
                # titre
                self.assertIsNotNone(question.get("titre"))
                #choix
                self.assertIsNotNone(question.get("choix"))
                # réponse
                self.assertIsNotNone(question.get("réponse"))
                # une seule bonne réponse
                self.assertNotIsInstance(question["réponse"],tuple)



unittest.main()
