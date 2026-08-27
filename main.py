from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.popup import Popup


# ============================================================
# COULEURS
# ============================================================

BLEU = (0.06, 0.36, 0.62, 1)
BLEU_FONCE = (0.025, 0.16, 0.30, 1)
BLANC = (1, 1, 1, 1)
GRIS = (0.94, 0.95, 0.97, 1)
GRIS_TEXTE = (0.35, 0.39, 0.43, 1)

VERT = (0.08, 0.52, 0.34, 1)
ORANGE = (0.90, 0.52, 0.08, 1)
VIOLET = (0.40, 0.25, 0.65, 1)
ROUGE = (0.75, 0.15, 0.15, 1)


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
        self.font_size = dp(16)

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
# CARTE MENU
# ============================================================

class CarteMenu(BoxLayout):

    def __init__(
        self,
        titre,
        sous_titre,
        couleur,
        icone,
        fonction,
        **kwargs
    ):

        super().__init__(
            orientation="vertical",
            spacing=dp(2),
            padding=[
                dp(8),
                dp(6),
                dp(8),
                dp(6)
            ],
            size_hint_y=None,
            height=dp(82),
            **kwargs
        )

        with self.canvas.before:

            Color(*GRIS)

            self.rectangle = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(17)]
            )

        self.bind(
            pos=self.actualiser,
            size=self.actualiser
        )

        bouton = BoutonModerne(
            text=icone + "  " + titre,
            couleur=couleur,
            size_hint_y=None,
            height=dp(46)
        )

        bouton.bind(
            on_release=fonction
        )

        self.add_widget(bouton)

        label = Label(
            text=sous_titre,
            color=GRIS_TEXTE,
            font_size=dp(9),
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

        self.add_widget(label)

    def actualiser(self, *args):

        self.rectangle.pos = self.pos
        self.rectangle.size = self.size


# ============================================================
# MENU PRINCIPAL
# ============================================================

class MainScreen(BoxLayout):

    def __init__(self, app, **kwargs):

        super().__init__(**kwargs)

        self.app = app

        self.orientation = "vertical"

        self.padding = [
            dp(12),
            dp(7),
            dp(12),
            dp(7)
        ]

        self.spacing = dp(6)

        # ====================================================
        # EN-TÊTE
        # ====================================================

        header = BoxLayout(
            orientation="vertical",
            spacing=0,
            size_hint_y=None,
            height=dp(78)
        )

        logo = Label(
            text="🩻",
            font_size=dp(25),
            size_hint_y=None,
            height=dp(29),
            color=BLEU
        )

        header.add_widget(logo)

        titre = Label(
            text="ECHOGRAPHIE NAYE",
            font_size=dp(22),
            bold=True,
            color=BLEU_FONCE,
            size_hint_y=None,
            height=dp(30),
            halign="center",
            valign="middle"
        )

        titre.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                value
            )
        )

        header.add_widget(titre)

        sous_titre = Label(
            text="Cabinet d'échographie • Gestion médicale",
            font_size=dp(9),
            color=GRIS_TEXTE,
            size_hint_y=None,
            height=dp(18),
            halign="center",
            valign="middle"
        )

        sous_titre.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                value
            )
        )

        header.add_widget(sous_titre)

        self.add_widget(header)

        # ====================================================
        # LIGNE
        # ====================================================

        ligne = BoxLayout(
            size_hint_y=None,
            height=dp(2)
        )

        with ligne.canvas.before:

            Color(*BLEU)

            rectangle = RoundedRectangle(
                pos=ligne.pos,
                size=ligne.size,
                radius=[dp(2)]
            )

        ligne.bind(
            pos=lambda obj, value:
            setattr(rectangle, "pos", value),
            size=lambda obj, value:
            setattr(rectangle, "size", value)
        )

        self.add_widget(ligne)

        # ====================================================
        # TITRE MENU
        # ====================================================

        self.add_widget(
            Label(
                text="MENU PRINCIPAL",
                color=BLEU_FONCE,
                font_size=dp(13),
                bold=True,
                size_hint_y=None,
                height=dp(25)
            )
        )

        # ====================================================
        # MENU
        # ====================================================

        menu = BoxLayout(
            orientation="vertical",
            spacing=dp(6),
            size_hint_y=None
        )

        menu.bind(
            minimum_height=menu.setter("height")
        )

        menu.add_widget(
            CarteMenu(
                "PATIENTS",
                "Gestion des patients",
                BLEU,
                "👤",
                self.ouvrir_patients
            )
        )

        menu.add_widget(
            CarteMenu(
                "ECHOGRAPHIE",
                "Créer et consulter les examens",
                VERT,
                "🩻",
                self.ouvrir_echographie
            )
        )

        menu.add_widget(
            CarteMenu(
                "CAISSE",
                "Gestion des paiements",
                ORANGE,
                "💰",
                self.ouvrir_caisse
            )
        )

        menu.add_widget(
            CarteMenu(
                "RAPPORTS",
                "Statistiques et activité",
                VIOLET,
                "📊",
                self.ouvrir_rapports
            )
        )

        menu.add_widget(
            CarteMenu(
                "PARAMÈTRES",
                "Configuration de l'application",
                BLEU_FONCE,
                "⚙️",
                self.ouvrir_parametres
            )
        )

        self.add_widget(menu)

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

        pied = Label(
            text="ECHOGRAPHIE NAYE • Gestion médicale",
            color=GRIS_TEXTE,
            font_size=dp(8),
            size_hint_y=None,
            height=dp(16)
        )

        self.add_widget(pied)

    # ========================================================
    # NAVIGATION
    # ========================================================

    def ouvrir_patients(self, instance):
        self.app.afficher_patients()

    def ouvrir_echographie(self, instance):
        self.app.afficher_echographie()

    def ouvrir_caisse(self, instance):
        self.app.afficher_caisse()

    def ouvrir_rapports(self, instance):
        self.app.afficher_rapports()

    def ouvrir_parametres(self, instance):
        self.app.afficher_parametres()


# ============================================================
# APPLICATION
# ============================================================

class EchographieNayeApp(App):

    def build(self):

        # IMPORTANT :
        # Le logiciel normal doit être lancé depuis login.py.
        return MainScreen(self)

    # ========================================================
    # FONCTION CENTRALE POUR CHANGER D'ÉCRAN
    # ========================================================

    def changer_ecran(self, ecran):

        self.root.clear_widgets()
        self.root.add_widget(ecran)

    # ========================================================
    # MENU
    # ========================================================

    def afficher_menu(self):

        self.changer_ecran(
            MainScreen(self)
        )

    # ========================================================
    # ERREUR
    # ========================================================

    def afficher_erreur(self, titre, erreur):

        print("ERREUR :", erreur)

        contenu = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(15)
        )

        message = Label(
            text=(
                "Impossible d'ouvrir ce module.\n\n"
                + str(erreur)
            ),
            color=ROUGE,
            font_size=dp(15),
            halign="center",
            valign="middle"
        )

        message.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                value
            )
        )

        contenu.add_widget(message)

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

    # ========================================================
    # PATIENTS
    # ========================================================

    def afficher_patients(self):

        try:

            from patients import PatientsScreen

            ecran = PatientsScreen(self)

            self.changer_ecran(ecran)

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

            ecran = EchographieScreen(self)

            self.changer_ecran(ecran)

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

            ecran = CaisseScreen(self)

            self.changer_ecran(ecran)

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

            ecran = RapportScreen(self)

            self.changer_ecran(ecran)

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

            ecran = ParametresScreen(self)

            self.changer_ecran(ecran)

        except Exception as erreur:

            self.afficher_erreur(
                "ERREUR PARAMÈTRES",
                erreur
            )


# ============================================================
# LANCEMENT DIRECT
# ============================================================

if __name__ == "__main__":

    EchographieNayeApp().run()