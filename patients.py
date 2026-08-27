import sqlite3
from datetime import datetime

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup


DB_NAME = "echographie_naye.db"


# ==============================
# COULEURS
# ==============================

BLEU = (0.08, 0.40, 0.70, 1)
BLEU_FONCE = (0.04, 0.25, 0.45, 1)
VERT = (0.10, 0.55, 0.35, 1)
ROUGE = (0.75, 0.15, 0.15, 1)
BLANC = (1, 1, 1, 1)
GRIS = (0.95, 0.96, 0.98, 1)


class PatientsScreen(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app

        self.orientation = "vertical"
        self.padding = dp(15)
        self.spacing = dp(10)

        # ==============================
        # EN-TÊTE
        # ==============================

        header = BoxLayout(
            size_hint_y=None,
            height=dp(70),
            padding=[dp(10), dp(5)]
        )

        titre = Label(
            text="👤  PATIENTS",
            font_size="27sp",
            bold=True,
            color=BLEU_FONCE
        )

        header.add_widget(titre)

        self.add_widget(header)

        # ==============================
        # ZONE DÉFILABLE
        # ==============================

        scroll = ScrollView(
            do_scroll_x=False
        )

        contenu = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=[dp(5), dp(5), dp(5), dp(20)],
            size_hint_y=None
        )

        contenu.bind(
            minimum_height=contenu.setter("height")
        )

        # ==============================
        # INFORMATIONS DU PATIENT
        # ==============================

        section = Label(
            text="Informations du patient",
            font_size="20sp",
            bold=True,
            color=BLEU_FONCE,
            size_hint_y=None,
            height=dp(45),
            halign="left"
        )

        contenu.add_widget(section)

        self.nom = self.creer_champ(
            "Nom du patient"
        )

        self.prenom = self.creer_champ(
            "Prénom du patient"
        )

        self.age = self.creer_champ(
            "Âge",
            input_filter="int"
        )

        self.sexe = self.creer_champ(
            "Sexe : Homme / Femme"
        )

        self.telephone = self.creer_champ(
            "Téléphone"
        )

        self.adresse = self.creer_champ(
            "Adresse"
        )

        contenu.add_widget(self.nom)
        contenu.add_widget(self.prenom)
        contenu.add_widget(self.age)
        contenu.add_widget(self.sexe)
        contenu.add_widget(self.telephone)
        contenu.add_widget(self.adresse)

        # ==============================
        # MESSAGE
        # ==============================

        self.message = Label(
            text="",
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )

        contenu.add_widget(self.message)

        # ==============================
        # BOUTON ENREGISTRER
        # ==============================

        enregistrer = Button(
            text="✓  ENREGISTRER LE PATIENT",
            font_size="19sp",
            bold=True,
            color=BLANC,
            background_normal="",
            background_color=VERT,
            size_hint_y=None,
            height=dp(60)
        )

        enregistrer.bind(
            on_press=self.enregistrer_patient
        )

        contenu.add_widget(enregistrer)

        # ==============================
        # BOUTON LISTE
        # ==============================

        liste = Button(
            text="☷  LISTE DES PATIENTS",
            font_size="19sp",
            bold=True,
            color=BLANC,
            background_normal="",
            background_color=BLEU,
            size_hint_y=None,
            height=dp(60)
        )

        liste.bind(
            on_press=self.afficher_liste
        )

        contenu.add_widget(liste)

        scroll.add_widget(contenu)

        self.add_widget(scroll)

        # ==============================
        # RETOUR
        # ==============================

        retour = Button(
            text="←  RETOUR AU MENU",
            font_size="18sp",
            bold=True,
            color=BLANC,
            background_normal="",
            background_color=BLEU_FONCE,
            size_hint_y=None,
            height=dp(58)
        )

        retour.bind(
            on_press=self.retour
        )

        self.add_widget(retour)

    # ==============================
    # CRÉER UN CHAMP
    # ==============================

    def creer_champ(self, texte, input_filter=None):

        champ = TextInput(
            hint_text=texte,
            font_size="18sp",
            multiline=False,
            size_hint_y=None,
            height=dp(58),
            padding=[dp(15), dp(15)]
        )

        if input_filter:
            champ.input_filter = input_filter

        return champ

    # ==============================
    # ENREGISTRER
    # ==============================

    def enregistrer_patient(self, instance):

        nom = self.nom.text.strip()
        prenom = self.prenom.text.strip()
        age = self.age.text.strip()
        sexe = self.sexe.text.strip()
        telephone = self.telephone.text.strip()
        adresse = self.adresse.text.strip()

        if not nom:
            self.message.text = "⚠ Veuillez saisir le nom."
            self.message.color = ROUGE
            return

        try:

            conn = sqlite3.connect(DB_NAME)

            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT,
                    age TEXT,
                    sexe TEXT,
                    telephone TEXT,
                    adresse TEXT,
                    date_enregistrement TEXT
                )
            """)

            date = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            cursor.execute("""
                INSERT INTO patients
                (
                    nom,
                    prenom,
                    age,
                    sexe,
                    telephone,
                    adresse,
                    date_enregistrement
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                nom,
                prenom,
                age,
                sexe,
                telephone,
                adresse,
                date
            ))

            conn.commit()
            conn.close()

            self.message.text = "✓ Patient enregistré avec succès."
            self.message.color = VERT

            self.effacer_champs()

        except Exception as erreur:

            self.message.text = "Erreur d'enregistrement."
            self.message.color = ROUGE

            print("ERREUR PATIENT :", erreur)

    # ==============================
    # EFFACER
    # ==============================

    def effacer_champs(self):

        self.nom.text = ""
        self.prenom.text = ""
        self.age.text = ""
        self.sexe.text = ""
        self.telephone.text = ""
        self.adresse.text = ""

    # ==============================
    # LISTE DES PATIENTS
    # ==============================

    def afficher_liste(self, instance):

        self.ouvrir_liste_patients()

    # ==============================
    # OUVRIR / ACTUALISER LA LISTE
    # ==============================

    def ouvrir_liste_patients(self):

        try:

            conn = sqlite3.connect(DB_NAME)

            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, nom, prenom, age, sexe, telephone
                FROM patients
                ORDER BY id DESC
            """)

            patients = cursor.fetchall()

            conn.close()

        except Exception as erreur:

            print("ERREUR LISTE :", erreur)
            return

        contenu = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15),
            size_hint_y=None
        )

        contenu.bind(
            minimum_height=contenu.setter("height")
        )

        titre = Label(
            text="LISTE DES PATIENTS",
            font_size="23sp",
            bold=True,
            color=BLEU_FONCE,
            size_hint_y=None,
            height=dp(55)
        )

        contenu.add_widget(titre)

        if not patients:

            contenu.add_widget(
                Label(
                    text="Aucun patient enregistré.",
                    font_size="18sp",
                    size_hint_y=None,
                    height=dp(60)
                )
            )

        else:

            for patient in patients:

                identifiant = patient[0]
                nom = patient[1] or ""
                prenom = patient[2] or ""
                age = patient[3] or ""
                sexe = patient[4] or ""
                telephone = patient[5] or ""

                # ------------------------------------------
                # CARTE PATIENT
                # ------------------------------------------

                carte = BoxLayout(
                    orientation="vertical",
                    spacing=dp(5),
                    padding=dp(8),
                    size_hint_y=None,
                    height=dp(125)
                )

                texte = (
                    f"#{identifiant}  {nom} {prenom}\n"
                    f"Âge : {age}    Sexe : {sexe}\n"
                    f"Téléphone : {telephone}"
                )

                label = Label(
                    text=texte,
                    font_size="16sp",
                    halign="left",
                    valign="middle",
                    color=BLEU_FONCE
                )

                label.bind(
                    size=lambda obj, value:
                    setattr(
                        obj,
                        "text_size",
                        value
                    )
                )

                carte.add_widget(label)

                # ------------------------------------------
                # BOUTON SUPPRIMER
                # ------------------------------------------

                supprimer = Button(
                    text="🗑️  SUPPRIMER PATIENT",
                    font_size="15sp",
                    bold=True,
                    background_normal="",
                    background_color=ROUGE,
                    color=BLANC,
                    size_hint_y=None,
                    height=dp(42)
                )

                supprimer.bind(
                    on_press=lambda btn,
                    pid=identifiant,
                    nom_patient=f"{nom} {prenom}":
                    self.confirmer_suppression(
                        pid,
                        nom_patient,
                        popup
                    )
                )

                carte.add_widget(supprimer)

                contenu.add_widget(carte)

        scroll = ScrollView(
            do_scroll_x=False
        )

        scroll.add_widget(contenu)

        fermer = Button(
            text="FERMER",
            font_size="18sp",
            bold=True,
            color=BLANC,
            background_normal="",
            background_color=BLEU_FONCE,
            size_hint_y=None,
            height=dp(55)
        )

        boite = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        boite.add_widget(scroll)
        boite.add_widget(fermer)

        popup = Popup(
            title="Patients enregistrés",
            content=boite,
            size_hint=(0.95, 0.90)
        )

        fermer.bind(
            on_press=popup.dismiss
        )

        popup.open()

    # ==============================
    # CONFIRMATION SUPPRESSION
    # ==============================

    def confirmer_suppression(
        self,
        patient_id,
        nom_patient,
        popup_liste
    ):

        contenu = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(15)
        )

        texte = Label(
            text=(
                "Voulez-vous vraiment supprimer\n"
                f"le patient :\n{nom_patient} ?"
            ),
            font_size="18sp",
            bold=True,
            color=BLEU_FONCE,
            halign="center",
            valign="middle"
        )

        texte.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                value
            )
        )

        contenu.add_widget(texte)

        boutons = BoxLayout(
            spacing=dp(10),
            size_hint_y=None,
            height=dp(55)
        )

        annuler = Button(
            text="ANNULER",
            font_size="16sp",
            bold=True,
            background_normal="",
            background_color=BLEU_FONCE,
            color=BLANC
        )

        supprimer = Button(
            text="SUPPRIMER",
            font_size="16sp",
            bold=True,
            background_normal="",
            background_color=ROUGE,
            color=BLANC
        )

        boutons.add_widget(annuler)
        boutons.add_widget(supprimer)

        contenu.add_widget(boutons)

        popup_confirmation = Popup(
            title="CONFIRMATION",
            content=contenu,
            size_hint=(0.90, 0.40),
            auto_dismiss=False
        )

        annuler.bind(
            on_press=popup_confirmation.dismiss
        )

        supprimer.bind(
            on_press=lambda btn:
            self.supprimer_patient(
                patient_id,
                popup_confirmation,
                popup_liste
            )
        )

        popup_confirmation.open()

    # ==============================
    # SUPPRIMER PATIENT
    # ==============================

    def supprimer_patient(
        self,
        patient_id,
        popup_confirmation,
        popup_liste
    ):

        try:

            conn = sqlite3.connect(DB_NAME)

            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM patients
                WHERE id = ?
                """,
                (patient_id,)
            )

            conn.commit()
            conn.close()

            popup_confirmation.dismiss()
            popup_liste.dismiss()

            self.message.text = (
                "✓ Patient supprimé avec succès."
            )

            self.message.color = VERT

            # Réouvrir automatiquement la liste
            self.ouvrir_liste_patients()

        except Exception as erreur:

            print(
                "ERREUR SUPPRESSION PATIENT :",
                erreur
            )

            popup_confirmation.dismiss()

            self.message.text = (
                "Erreur lors de la suppression."
            )

            self.message.color = ROUGE

    # ==============================
    # RETOUR
    # ==============================

    def retour(self, instance):

        self.app.afficher_menu()