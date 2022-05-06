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
import sys


def FromData(json_ch):
    json_data = open(json_ch, "r")
    # Charge le fichier JSON
    data = json.loads(json_data.read())
    # Affiche la catégorie et la difficulté
    print(f"CATEGORIE : {data['categorie']}  DIFFICULTE : {data['difficulte']}")
    print("")
    # Affiche le sujet du Questionnaire
    print(f"Sujet : {data['titre']}")
    print("")
    # affiche le nombre total de question
    print(f"{len(data['questions'])} questions")
    print("")
    # initialise le compteur de question
    n_question = 0
    # creer la liste des questions
    questions = []
    for question in data["questions"]:
        # incrémente le compteur de question
        n_question += 1
        # remplis la liste des questions
        questions.append(
            Question(question["titre"], question["choix"], question["réponse"], len(data["questions"]), n_question))
    return questions


class Question:
    def __init__(self, titre, choix, bonne_reponse, nb_tot_question, n_question):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse
        self.n_question = n_question
        self.nb_tot_question = nb_tot_question

    def poser(self):
        # affiche la question ainsi que sa numérotation
        print(f"QUESTION -- n°{self.n_question}/{self.nb_tot_question}")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i + 1, "-", self.choix[i])

        print()
        # demande une réponse numérique a l'utilisateur
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        # Determine si la réponse donné est correcte ou non
        if self.choix[reponse_int - 1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
        print()
        # renvoie si la réponse est correcte ou non
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
        # initialisation du compteur score
        score = 0
        for question in self.questions:
            if question.poser():
                # incrementation du compteur score
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


# Chemin du fichier JSON contenant le questionnaire

# on regarde si un argument à été donné lors du lancement
if len(sys.argv) > 1:
    # si oui  on verifie que l'argument est bien un fichier qui s'ouvre.
    try:
        fichier = open(sys.argv[1], "r")
        fichier.close()
        # l'argument deviens le chemin du fichier
        json_ch = sys.argv[1]
    except:
        print("ERREUR : Pas de fichier trouvé sur ce chemin")
        sys.exit()

else:
    json_ch = "animaux_leschats_confirme.json"

# lancement du questionnaire
Questionnaire(FromData(json_ch)).lancer()
