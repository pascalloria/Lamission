# PROJET QUESTIONNAIRE V3 : POO
#
# - Pratiquer sur la POO
# - Travailler sur du code existant
# - Mener un raisonnement
#
# -> Définir les entitées (données, actions)
#
# Question
#    - titre       - str
#    - choix       - (str)
#    - bonne_reponse   - str
#
#    - poser()  -> bool
#
# Questionnaire
#    - questions      - (Question)
#
#    - lancer()
#
import json


def FromData(json_data):
    # Charge le fichier JSON
    data = json.loads(json_data.read())
    # Affiche la catégorie et la difficulté
    print(f"CATEGORIE : {data['categorie']}  DIFFICULTE : {data['difficulte']}")
    print("")
    # Affiche le sujet du Questionnaire
    print(f"Sujet : {data['titre']}")
    print("")

    question_data = data["questions"]
    print(f"{len(question_data)} questions")
    print("")
    questions = []
    n_question = 0
    for question in question_data:
        n_question += 1
        questions.append(Question(question["titre"], question["choix"], question["réponse"],len(question_data),n_question))
    return questions

class Question:
    def __init__(self, titre, choix, bonne_reponse,nb_tot_question,n_question):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse
        self.n_question=n_question
        self.nb_tot_question=nb_tot_question


    def poser(self):
        print(f"QUESTION -- n°{self.n_question}/{self.nb_tot_question}")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i + 1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int - 1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")

        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)


class Questionnaire:
    def __init__(self, questions):
        self.questions = questions

    def lancer(self):
        score = 0
        for question in self.questions:
            if question.poser():
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


json_data = open("animaux_leschats_confirme.json", "r")

Questionnaire(FromData(json_data)).lancer()
