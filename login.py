from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.popup import Popup


# ============================================================
# COULEURS
# ============================================================

BLEU = (0.06, 0.36, 0.62, 1)
BLEU_FONCE = (0.025, 0.16, 0.30, 1)

VERT = (0.08, 0.52, 0.34, 1)
ROUGE = (0.75, 0.15, 0.15, 1)

BLANC = (1, 1, 1, 1)

GRIS = (0.94, 0.95, 0.97, 1)
GRIS_TEXTE = (0.35, 0.39, 0.43, 1)


# ============================================================
# BOUTON MODERNE
# ============================================================

class BoutonModerne(Button):

    def __init__(self, couleur=BLEU, **kwargs):

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        self.color = BLANC
        self.bold = True
        self.font_size = dp(17)

        with self.canvas.before:

            Color(*couleur)

            self.rectangle = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(16)]
            )

        self.bind(
            pos=self.actualiser,
            size=self.actualiser
        )

    def actualiser(self, *args):

        self.rectangle.pos = self.pos
        self.rectangle.size = self.size


# ============================================================
# LOGIN
# ============================================================

class LoginScreen(BoxLayout):

    def __init__(self, app, **kwargs):

        super().__init__(**kwargs)

        self.app = app

        self.orientation = "vertical"

        self.padding = [
            dp(25),
            dp(20),
            dp(25),
            dp(20)
        ]

        self.spacing = dp(12)

        # ====================================================
        # ESPACE HAUT
        # ====================================================

        self.add_widget(
            Label(
                text="",
                size_hint_y=0.20
            )
        )

        # ====================================================
        # LOGO
        # ====================================================

        self.add_widget(
            Label(
                text="🩻",
                font_size=dp(42),
                size_hint_y=None,
                height=dp(55)
            )
        )

        # ====================================================
        # TITRE
        # ====================================================

        titre = Label(
            text="ECHOGRAPHIE NAYE",
            font_size=dp(24),
            bold=True,
            color=BLEU_FONCE,
            size_hint_y=None,
            height=dp(50),
            halign="center",
            valign="middle"
        )

        titre.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        self.add_widget(titre)

        # ====================================================
        # SOUS TITRE
        # ====================================================

        self.add_widget(
            Label(
                text="Connexion à votre espace",
                font_size=dp(14),
                color=GRIS_TEXTE,
                size_hint_y=None,
                height=dp(30)
            )
        )

        # ====================================================
        # NOM UTILISATEUR
        # ====================================================

        self.nom = TextInput(
            hint_text="Nom d'utilisateur",
            font_size=dp(17),
            multiline=False,
            size_hint_y=None,
            height=dp(55),
            padding=[
                dp(15),
                dp(15)
            ],
            background_normal="",
            background_color=GRIS
        )

        self.add_widget(self.nom)

        # ====================================================
        # MOT DE PASSE
        # ====================================================

        self.mot_de_passe = TextInput(
            hint_text="Mot de passe",
            font_size=dp(17),
            multiline=False,
            password=True,
            size_hint_y=None,
            height=dp(55),
            padding=[
                dp(15),
                dp(15)
            ],
            background_normal="",
            background_color=GRIS
        )

        self.add_widget(self.mot_de_passe)

        # ====================================================
        # MESSAGE
        # ====================================================

        self.message = Label(
            text="",
            font_size=dp(14),
            bold=True,
            size_hint_y=None,
            height=dp(35)
        )

        self.add_widget(self.message)

        # ====================================================
        # CONNEXION
        # ====================================================

        connexion = BoutonModerne(
            text="🔐  SE CONNECTER",
            couleur=VERT,
            size_hint_y=None,
            height=dp(58)
        )

        connexion.bind(
            on_release=self.connecter
        )

        self.add_widget(connexion)

        # ====================================================
        # ESPACE
        # ====================================================

        self.add_widget(
            Label(
                text="",
                size_hint_y=1
            )
        )

        # ====================================================
        # PIED
        # ====================================================

        self.add_widget(
            Label(
                text="ECHOGRAPHIE NAYE • Gestion médicale",
                font_size=dp(10),
                color=GRIS_TEXTE,
                size_hint_y=None,
                height=dp(20)
            )
        )

    # ========================================================
    # CONNEXION
    # ========================================================

    def connecter(self, instance):

        nom = self.nom.text.strip()
        mot_de_passe = self.mot_de_passe.text.strip()

        if nom == "Amira" and mot_de_passe == "2303":

            self.message.text = "✓ Connexion réussie"
            self.message.color = VERT

            self.app.afficher_menu()

        else:

            self.message.text = (
                "⚠ Nom d'utilisateur ou mot de passe incorrect."
            )

            self.message.color = ROUGE

            self.mot_de_passe.text = ""


# ============================================================
# APPLICATION
# ============================================================

class LoginApp(App):

    def build(self):

        return LoginScreen(self)

    # ========================================================
    # MENU PRINCIPAL
    # ========================================================

    def afficher_menu(self):

        try:

            from main import MainScreen

            self.root.clear_widgets()

            self.root.add_widget(
                MainScreen(self)
            )

        except Exception as erreur:

            self.afficher_erreur(
                "ERREUR MENU",
                erreur
            )

    # ========================================================
    # PATIENTS
    # ========================================================

    def afficher_patients(self):

        try:

            from patients import PatientsScreen

            self.root.clear_widgets()

            self.root.add_widget(
                PatientsScreen(self)
            )

        except Exception as erreur:

            self.afficher_erreur(
                "ERREUR PATIENTS",
                erreur
            )

    # ========================================================
    # ECHOGRAPHIE
    # ========================================================

    def afficher_echographie(self):

        try:

            from echographie import EchographieScreen

            self.root.clear_widgets()

            self.root.add_widget(
                EchographieScreen(self)
            )

        except Exception as erreur:

            self.afficher_erreur(
                "ERREUR ÉCHOGRAPHIE",
                erreur
            )

    # ========================================================
    # CAISSE
    # ========================================================

    def afficher_caisse(self):

        try:

            from caisse import CaisseScreen

            self.root.clear_widgets()

            self.root.add_widget(
                CaisseScreen(self)
            )

        except Exception as erreur:

            self.afficher_erreur(
                "ERREUR CAISSE",
                erreur
            )

    # ========================================================
    # RAPPORTS
    # ========================================================

    def afficher_rapports(self):

        try:

            from rapports import RapportScreen

            self.root.clear_widgets()

            self.root.add_widget(
                RapportScreen(self)
            )

        except Exception as erreur:

            self.afficher_erreur(
                "ERREUR RAPPORTS",
                erreur
            )

    # ========================================================
    # PARAMÈTRES
    # ========================================================

    def afficher_parametres(self):

        try:

            from parametres import ParametresScreen

            self.root.clear_widgets()

            self.root.add_widget(
                ParametresScreen(self)
            )

        except Exception as erreur:

            self.afficher_erreur(
                "ERREUR PARAMÈTRES",
                erreur
            )

    # ========================================================
    # MESSAGE D'ERREUR
    # ========================================================

    def afficher_erreur(self, titre, erreur):

        print("ERREUR :", erreur)

        contenu = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(15)
        )

        label = Label(
            text=str(erreur),
            font_size=dp(15),
            color=ROUGE,
            halign="center",
            valign="middle"
        )

        label.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                value
            )
        )

        contenu.add_widget(label)

        fermer = BoutonModerne(
            text="FERMER",
            couleur=BLEU_FONCE,
            size_hint_y=None,
            height=dp(52)
        )

        contenu.add_widget(fermer)

        popup = Popup(
            title=titre,
            content=contenu,
            size_hint=(0.90, 0.45)
        )

        fermer.bind(
            on_release=popup.dismiss
        )

        popup.open()


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":

    LoginApp().run()