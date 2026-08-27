from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView


# ============================================================
# COULEURS
# ============================================================

BLEU = (0.08, 0.40, 0.70, 1)
BLEU_FONCE = (0.04, 0.25, 0.45, 1)
VERT = (0.10, 0.55, 0.35, 1)
ROUGE = (0.75, 0.15, 0.15, 1)
GRIS = (0.95, 0.96, 0.97, 1)
BLANC = (1, 1, 1, 1)


# ============================================================
# PARAMETRES
# ============================================================

class ParametresScreen(BoxLayout):

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

        # ----------------------------------------------------
        # EN-TÊTE
        # ----------------------------------------------------

        titre = Label(
            text="⚙ PARAMÈTRES",
            font_size="27sp",
            bold=True,
            color=BLEU_FONCE,
            size_hint_y=None,
            height=dp(65)
        )

        self.add_widget(titre)

        # ----------------------------------------------------
        # SCROLL
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # INFORMATIONS DU CABINET
        # ----------------------------------------------------

        contenu.add_widget(
            Label(
                text="INFORMATIONS",
                font_size="21sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(50)
            )
        )

        contenu.add_widget(
            Label(
                text="Nom de l'établissement",
                font_size="17sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(40)
            )
        )

        self.nom = TextInput(
            text="ECHOGRAPHIE NAYE",
            font_size="18sp",
            multiline=False,
            size_hint_y=None,
            height=dp(55)
        )

        contenu.add_widget(self.nom)

        contenu.add_widget(
            Label(
                text="Téléphone",
                font_size="17sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(40)
            )
        )

        self.telephone = TextInput(
            hint_text="Numéro de téléphone",
            font_size="18sp",
            multiline=False,
            size_hint_y=None,
            height=dp(55)
        )

        contenu.add_widget(self.telephone)

        contenu.add_widget(
            Label(
                text="Adresse",
                font_size="17sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(40)
            )
        )

        self.adresse = TextInput(
            hint_text="Adresse de l'établissement",
            font_size="18sp",
            multiline=False,
            size_hint_y=None,
            height=dp(55)
        )

        contenu.add_widget(self.adresse)

        # ----------------------------------------------------
        # TARIF
        # ----------------------------------------------------

        contenu.add_widget(
            Label(
                text="TARIF PAR DÉFAUT",
                font_size="21sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(50)
            )
        )

        self.tarif = TextInput(
            hint_text="Prix en FCFA",
            text="0",
            font_size="18sp",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(55)
        )

        contenu.add_widget(self.tarif)

        # ----------------------------------------------------
        # MESSAGE
        # ----------------------------------------------------

        self.message = Label(
            text="",
            font_size="16sp",
            bold=True,
            color=VERT,
            size_hint_y=None,
            height=dp(45)
        )

        contenu.add_widget(self.message)

        # ----------------------------------------------------
        # ENREGISTRER
        # ----------------------------------------------------

        enregistrer = Button(
            text="✓ ENREGISTRER LES PARAMÈTRES",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(60),
            background_normal="",
            background_color=VERT,
            color=BLANC
        )

        enregistrer.bind(
            on_press=self.enregistrer
        )

        contenu.add_widget(enregistrer)

        # ----------------------------------------------------
        # RÉINITIALISER
        # ----------------------------------------------------

        reinitialiser = Button(
            text="↻ RÉINITIALISER",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(55),
            background_normal="",
            background_color=ROUGE,
            color=BLANC
        )

        reinitialiser.bind(
            on_press=self.reinitialiser
        )

        contenu.add_widget(reinitialiser)

        scroll.add_widget(contenu)

        self.add_widget(scroll)

        # ----------------------------------------------------
        # RETOUR
        # ----------------------------------------------------

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
    # ENREGISTRER
    # ========================================================

    def enregistrer(self, instance):

        self.message.text = "✓ Paramètres enregistrés."
        self.message.color = VERT

        print("PARAMÈTRES :")
        print("Nom :", self.nom.text)
        print("Téléphone :", self.telephone.text)
        print("Adresse :", self.adresse.text)
        print("Tarif :", self.tarif.text)

    # ========================================================
    # RÉINITIALISER
    # ========================================================

    def reinitialiser(self, instance):

        self.nom.text = "ECHOGRAPHIE NAYE"
        self.telephone.text = ""
        self.adresse.text = ""
        self.tarif.text = "0"

        self.message.text = "Paramètres réinitialisés."
        self.message.color = BLEU

    # ========================================================
    # RETOUR AU MENU
    # ========================================================

    def retour(self, instance):

        self.app.afficher_menu()


# ============================================================
# TEST DIRECT
# ============================================================

if __name__ == "__main__":

    from kivy.app import App

    class ParametresApp(App):

        def build(self):

            return ParametresScreen(self)

    ParametresApp().run()