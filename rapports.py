import sqlite3

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


DB_NAME = "echographie_naye.db"


BLEU = (0.08, 0.40, 0.70, 1)
BLEU_FONCE = (0.04, 0.25, 0.45, 1)
VERT = (0.10, 0.55, 0.35, 1)
ROUGE = (0.75, 0.15, 0.15, 1)
ORANGE = (0.90, 0.50, 0.08, 1)
BLANC = (1, 1, 1, 1)


class RapportScreen(BoxLayout):

    def __init__(self, app, **kwargs):

        super().__init__(**kwargs)

        self.app = app

        self.orientation = "vertical"
        self.padding = dp(15)
        self.spacing = dp(10)

        self.construire_interface()

    # ========================================================
    # INTERFACE
    # ========================================================

    def construire_interface(self):

        titre = Label(
            text="📊 RAPPORTS",
            font_size="28sp",
            bold=True,
            color=BLEU_FONCE,
            size_hint_y=None,
            height=dp(65)
        )

        self.add_widget(titre)

        scroll = ScrollView(
            do_scroll_x=False
        )

        contenu = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(10),
            size_hint_y=None
        )

        contenu.bind(
            minimum_height=contenu.setter("height")
        )

        # ====================================================
        # JOURNALIER
        # ====================================================

        contenu.add_widget(
            Label(
                text="📅 JOURNALIER",
                font_size="21sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(50)
            )
        )

        patients_jour = self.nombre_patients(
            "date('now')"
        )

        recettes_jour = self.recettes(
            "date('now')"
        )

        depenses_jour = self.depenses(
            "date('now')"
        )

        benefice_jour = (
            recettes_jour - depenses_jour
        )

        contenu.add_widget(
            self.creer_ligne(
                "Nombre de patients",
                str(patients_jour),
                BLEU
            )
        )

        contenu.add_widget(
            self.creer_ligne(
                "Recettes",
                self.format_fcfa(recettes_jour),
                VERT
            )
        )

        contenu.add_widget(
            self.creer_ligne(
                "Bénéfice",
                self.format_fcfa(benefice_jour),
                BLEU_FONCE
            )
        )

        # ====================================================
        # HEBDOMADAIRE
        # ====================================================

        contenu.add_widget(
            Label(
                text="📆 HEBDOMADAIRE",
                font_size="21sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(50)
            )
        )

        patients_semaine = self.nombre_patients(
            "date('now', '-6 days')"
        )

        recettes_semaine = self.recettes(
            "date('now', '-6 days')"
        )

        depenses_semaine = self.depenses(
            "date('now', '-6 days')"
        )

        benefice_semaine = (
            recettes_semaine - depenses_semaine
        )

        contenu.add_widget(
            self.creer_ligne(
                "Nombre de patients",
                str(patients_semaine),
                BLEU
            )
        )

        contenu.add_widget(
            self.creer_ligne(
                "Recettes",
                self.format_fcfa(recettes_semaine),
                VERT
            )
        )

        contenu.add_widget(
            self.creer_ligne(
                "Bénéfice",
                self.format_fcfa(benefice_semaine),
                BLEU_FONCE
            )
        )

        # ====================================================
        # MENSUEL
        # ====================================================

        contenu.add_widget(
            Label(
                text="🗓 MENSUEL",
                font_size="21sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(50)
            )
        )

        patients_mois = self.nombre_patients(
            "date('now', 'start of month')"
        )

        recettes_mois = self.recettes(
            "date('now', 'start of month')"
        )

        depenses_mois = self.depenses(
            "date('now', 'start of month')"
        )

        benefice_mois = (
            recettes_mois - depenses_mois
        )

        contenu.add_widget(
            self.creer_ligne(
                "Nombre de patients",
                str(patients_mois),
                BLEU
            )
        )

        contenu.add_widget(
            self.creer_ligne(
                "Recettes",
                self.format_fcfa(recettes_mois),
                VERT
            )
        )

        contenu.add_widget(
            self.creer_ligne(
                "Bénéfice",
                self.format_fcfa(benefice_mois),
                BLEU_FONCE
            )
        )

        # ====================================================
        # TOTAL GÉNÉRAL
        # ====================================================

        contenu.add_widget(
            Label(
                text="📈 TOTAL GÉNÉRAL",
                font_size="21sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(50)
            )
        )

        nombre_patients_total = self.compter(
            "SELECT COUNT(*) FROM patients"
        )

        nombre_echographies = self.compter(
            "SELECT COUNT(*) FROM echographies"
        )

        recettes_total = self.total_prix()

        contenu.add_widget(
            self.creer_ligne(
                "Patients enregistrés",
                str(nombre_patients_total),
                BLEU
            )
        )

        contenu.add_widget(
            self.creer_ligne(
                "Échographies réalisées",
                str(nombre_echographies),
                ORANGE
            )
        )

        contenu.add_widget(
            self.creer_ligne(
                "Recettes totales",
                self.format_fcfa(recettes_total),
                VERT
            )
        )

        # ====================================================
        # TYPES
        # ====================================================

        contenu.add_widget(
            Label(
                text="TYPES D'ECHOGRAPHIES",
                font_size="20sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(50)
            )
        )

        types = self.obtenir_types()

        if not types:

            contenu.add_widget(
                Label(
                    text="Aucune échographie enregistrée.",
                    font_size="17sp",
                    color=BLEU_FONCE,
                    size_hint_y=None,
                    height=dp(60)
                )
            )

        else:

            for type_echo, nombre in types:

                contenu.add_widget(
                    Label(
                        text=(
                            str(type_echo)
                            + " : "
                            + str(nombre)
                            + " examen(s)"
                        ),
                        font_size="17sp",
                        color=BLEU_FONCE,
                        size_hint_y=None,
                        height=dp(45)
                    )
                )

        scroll.add_widget(contenu)

        self.add_widget(scroll)

        # ====================================================
        # ACTUALISER
        # ====================================================

        actualiser = Button(
            text="↻ ACTUALISER",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(55),
            background_normal="",
            background_color=VERT,
            color=BLANC
        )

        actualiser.bind(
            on_press=self.actualiser
        )

        self.add_widget(actualiser)

        # ====================================================
        # RETOUR
        # ====================================================

        retour = Button(
            text="← RETOUR AU MENU",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(58),
            background_normal="",
            background_color=BLEU_FONCE,
            color=BLANC
        )

        retour.bind(
            on_press=self.retour
        )

        self.add_widget(retour)

    # ========================================================
    # COMPTER
    # ========================================================

    def compter(self, requete):

        connexion = None

        try:

            connexion = sqlite3.connect(DB_NAME)

            curseur = connexion.cursor()

            curseur.execute(requete)

            resultat = curseur.fetchone()

            if resultat:

                return int(resultat[0] or 0)

            return 0

        except Exception as erreur:

            print(
                "ERREUR RAPPORT :",
                erreur
            )

            return 0

        finally:

            if connexion:

                connexion.close()

    # ========================================================
    # NOMBRE DE PATIENTS
    # ========================================================

    def nombre_patients(self, date_depart):

        connexion = None

        try:

            connexion = sqlite3.connect(DB_NAME)

            curseur = connexion.cursor()

            if date_depart == "date('now')":

                curseur.execute(
                    """
                    SELECT COUNT(DISTINCT patient_id)
                    FROM echographies
                    WHERE date(date_examen) = date('now')
                    """
                )

            else:

                curseur.execute(
                    """
                    SELECT COUNT(DISTINCT patient_id)
                    FROM echographies
                    WHERE date(date_examen) >=
                    """
                    + date_depart
                )

            resultat = curseur.fetchone()

            if resultat:

                return int(resultat[0] or 0)

            return 0

        except Exception as erreur:

            print(
                "ERREUR PATIENTS :",
                erreur
            )

            return 0

        finally:

            if connexion:

                connexion.close()

    # ========================================================
    # RECETTES
    # ========================================================

    def recettes(self, date_depart):

        connexion = None

        try:

            connexion = sqlite3.connect(DB_NAME)

            curseur = connexion.cursor()

            if date_depart == "date('now')":

                curseur.execute(
                    """
                    SELECT COALESCE(
                        SUM(CAST(prix AS REAL)),
                        0
                    )
                    FROM echographies
                    WHERE date(date_examen) = date('now')
                    """
                )

            else:

                curseur.execute(
                    """
                    SELECT COALESCE(
                        SUM(CAST(prix AS REAL)),
                        0
                    )
                    FROM echographies
                    WHERE date(date_examen) >=
                    """
                    + date_depart
                )

            resultat = curseur.fetchone()

            if resultat:

                return float(resultat[0] or 0)

            return 0

        except Exception as erreur:

            print(
                "ERREUR RECETTES :",
                erreur
            )

            return 0

        finally:

            if connexion:

                connexion.close()

    # ========================================================
    # DEPENSES
    # ========================================================

    def depenses(self, date_depart):

        connexion = None

        try:

            connexion = sqlite3.connect(DB_NAME)

            curseur = connexion.cursor()

            if date_depart == "date('now')":

                curseur.execute(
                    """
                    SELECT COALESCE(
                        SUM(montant),
                        0
                    )
                    FROM caisse
                    WHERE type = 'Dépense'
                    AND date(date_operation) = date('now')
                    """
                )

            else:

                curseur.execute(
                    """
                    SELECT COALESCE(
                        SUM(montant),
                        0
                    )
                    FROM caisse
                    WHERE type = 'Dépense'
                    AND date(date_operation) >=
                    """
                    + date_depart
                )

            resultat = curseur.fetchone()

            if resultat:

                return float(resultat[0] or 0)

            return 0

        except Exception as erreur:

            print(
                "ERREUR DEPENSES :",
                erreur
            )

            return 0

        finally:

            if connexion:

                connexion.close()

    # ========================================================
    # TOTAL PRIX
    # ========================================================

    def total_prix(self):

        connexion = None

        try:

            connexion = sqlite3.connect(DB_NAME)

            curseur = connexion.cursor()

            curseur.execute(
                """
                SELECT COALESCE(
                    SUM(CAST(prix AS REAL)),
                    0
                )
                FROM echographies
                """
            )

            resultat = curseur.fetchone()

            if resultat:

                return float(resultat[0] or 0)

            return 0

        except Exception as erreur:

            print(
                "ERREUR RECETTES :",
                erreur
            )

            return 0

        finally:

            if connexion:

                connexion.close()

    # ========================================================
    # TYPES
    # ========================================================

    def obtenir_types(self):

        connexion = None

        try:

            connexion = sqlite3.connect(DB_NAME)

            curseur = connexion.cursor()

            curseur.execute(
                """
                SELECT
                    type_echographie,
                    COUNT(*)
                FROM echographies
                GROUP BY type_echographie
                ORDER BY COUNT(*) DESC
                """
            )

            return curseur.fetchall()

        except Exception as erreur:

            print(
                "ERREUR TYPES :",
                erreur
            )

            return []

        finally:

            if connexion:

                connexion.close()

    # ========================================================
    # LIGNE STATISTIQUE
    # ========================================================

    def creer_ligne(
        self,
        titre,
        valeur,
        couleur
    ):

        ligne = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(70)
        )

        label_titre = Label(
            text=titre,
            font_size="16sp",
            bold=True,
            color=BLEU_FONCE,
            halign="left",
            valign="middle"
        )

        label_titre.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                value
            )
        )

        label_valeur = Label(
            text=valeur,
            font_size="18sp",
            bold=True,
            color=couleur,
            halign="right",
            valign="middle"
        )

        label_valeur.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                value
            )
        )

        ligne.add_widget(label_titre)
        ligne.add_widget(label_valeur)

        return ligne

    # ========================================================
    # FORMAT FCFA
    # ========================================================

    def format_fcfa(self, montant):

        try:

            return (
                f"{float(montant):,.0f}"
                .replace(",", " ")
                + " FCFA"
            )

        except Exception:

            return "0 FCFA"

    # ========================================================
    # ACTUALISER
    # ========================================================

    def actualiser(self, instance):

        self.clear_widgets()

        self.construire_interface()

    # ========================================================
    # RETOUR
    # ========================================================

    def retour(self, instance):

        self.app.afficher_menu()


# ============================================================
# TEST DIRECT
# ============================================================

if __name__ == "__main__":

    from kivy.app import App

    class RapportApp(App):

        def build(self):

            return RapportScreen(self)

    RapportApp().run()