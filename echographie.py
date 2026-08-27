import sqlite3
from datetime import datetime

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup


# ============================================================
# CONFIGURATION
# ============================================================

DB_NAME = "echographie_naye.db"


BLEU = (0.08, 0.40, 0.70, 1)
BLEU_FONCE = (0.04, 0.25, 0.45, 1)
VERT = (0.10, 0.55, 0.35, 1)
ROUGE = (0.75, 0.15, 0.15, 1)
ORANGE = (0.90, 0.50, 0.08, 1)
GRIS = (0.94, 0.95, 0.97, 1)
GRIS_FONCE = (0.25, 0.28, 0.30, 1)
BLANC = (1, 1, 1, 1)


# ============================================================
# ECHOGRAPHIE
# ============================================================

class EchographieScreen(BoxLayout):

    def __init__(self, app, **kwargs):

        super().__init__(**kwargs)

        self.app = app
        self.patient_id = None

        # ID de l'échographie actuellement modifiée
        self.examen_id_modification = None

        self.orientation = "vertical"
        self.padding = dp(15)
        self.spacing = dp(10)

        self.creer_table()
        self.construire_interface()


    # ========================================================
    # CONNEXION
    # ========================================================

    def connexion(self):

        return sqlite3.connect(DB_NAME)


    # ========================================================
    # TABLE ECHOGRAPHIES
    # ========================================================

    def creer_table(self):

        connexion = None

        try:

            connexion = self.connexion()
            curseur = connexion.cursor()

            curseur.execute("""
                CREATE TABLE IF NOT EXISTS echographies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER,
                    type_echographie TEXT,
                    motif TEXT,
                    observations TEXT,
                    conclusion TEXT,
                    prix TEXT,
                    date_examen TEXT
                )
            """)

            curseur.execute(
                "PRAGMA table_info(echographies)"
            )

            colonnes = [
                ligne[1]
                for ligne in curseur.fetchall()
            ]

            colonnes_necessaires = {
                "patient_id": "INTEGER",
                "type_echographie": "TEXT",
                "motif": "TEXT",
                "observations": "TEXT",
                "conclusion": "TEXT",
                "prix": "TEXT",
                "date_examen": "TEXT"
            }

            for nom, type_colonne in colonnes_necessaires.items():

                if nom not in colonnes:

                    curseur.execute(
                        f"""
                        ALTER TABLE echographies
                        ADD COLUMN {nom} {type_colonne}
                        """
                    )

            connexion.commit()

        except Exception as erreur:

            print(
                "ERREUR TABLE ECHOGRAPHIES :",
                erreur
            )

        finally:

            if connexion:
                connexion.close()


    # ========================================================
    # CRÉER / METTRE À JOUR TABLE CAISSE
    # ========================================================

    def preparer_caisse(self):

        connexion = None

        try:

            connexion = self.connexion()
            curseur = connexion.cursor()

            curseur.execute("""
                CREATE TABLE IF NOT EXISTS caisse (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    montant REAL DEFAULT 0,
                    type TEXT NOT NULL,
                    date_operation TEXT,
                    echographie_id INTEGER
                )
            """)

            curseur.execute(
                "PRAGMA table_info(caisse)"
            )

            colonnes = [
                ligne[1]
                for ligne in curseur.fetchall()
            ]

            if "echographie_id" not in colonnes:

                curseur.execute("""
                    ALTER TABLE caisse
                    ADD COLUMN echographie_id INTEGER
                """)

            connexion.commit()

        except Exception as erreur:

            print(
                "ERREUR PREPARATION CAISSE :",
                erreur
            )

        finally:

            if connexion:
                connexion.close()


    # ========================================================
    # INTERFACE
    # ========================================================

    def construire_interface(self):

        titre = Label(
            text="🩻 ECHOGRAPHIE NAYE",
            font_size="27sp",
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
        # PATIENT
        # ====================================================

        contenu.add_widget(
            Label(
                text="PATIENT",
                font_size="20sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(40)
            )
        )

        self.patient = Label(
            text="Aucun patient sélectionné",
            font_size="18sp",
            color=ROUGE,
            size_hint_y=None,
            height=dp(55)
        )

        contenu.add_widget(self.patient)


        bouton_patient = Button(
            text="CHOISIR UN PATIENT",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(60),
            background_normal="",
            background_color=BLEU,
            color=BLANC
        )

        bouton_patient.bind(
            on_press=self.choisir_patient
        )

        contenu.add_widget(bouton_patient)


        # ====================================================
        # TYPE
        # ====================================================

        contenu.add_widget(
            Label(
                text="TYPE D'ECHOGRAPHIE",
                font_size="20sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(45)
            )
        )

        self.type_echo = Spinner(
            text="Choisir le type",
            values=(
                "Obstétricale",
                "Pelvienne",
                "Abdominale",
                "Rénale",
                "Thyroïdienne",
                "Prostatique",
                "Mammaire",
                "Doppler",
                "Autre"
            ),
            font_size="18sp",
            size_hint_y=None,
            height=dp(60)
        )

        contenu.add_widget(self.type_echo)


        # ====================================================
        # MOTIF
        # ====================================================

        contenu.add_widget(
            Label(
                text="MOTIF",
                font_size="20sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(40)
            )
        )

        self.motif = TextInput(
            hint_text="Motif de l'examen",
            font_size="18sp",
            multiline=True,
            size_hint_y=None,
            height=dp(100)
        )

        contenu.add_widget(self.motif)


        # ====================================================
        # OBSERVATIONS
        # ====================================================

        contenu.add_widget(
            Label(
                text="OBSERVATIONS",
                font_size="20sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(40)
            )
        )

        self.observations = TextInput(
            hint_text="Observations...",
            font_size="18sp",
            multiline=True,
            size_hint_y=None,
            height=dp(180)
        )

        contenu.add_widget(self.observations)


        # ====================================================
        # CONCLUSION
        # ====================================================

        contenu.add_widget(
            Label(
                text="CONCLUSION",
                font_size="20sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(40)
            )
        )

        self.conclusion = TextInput(
            hint_text="Conclusion...",
            font_size="18sp",
            multiline=True,
            size_hint_y=None,
            height=dp(140)
        )

        contenu.add_widget(self.conclusion)


        # ====================================================
        # PRIX
        # ====================================================

        contenu.add_widget(
            Label(
                text="PRIX",
                font_size="20sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(40)
            )
        )

        self.prix = TextInput(
            hint_text="Prix en FCFA",
            font_size="18sp",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(58)
        )

        contenu.add_widget(self.prix)


        # ====================================================
        # MESSAGE
        # ====================================================

        self.message = Label(
            text="",
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height=dp(45)
        )

        contenu.add_widget(self.message)


        # ====================================================
        # BOUTON ENREGISTRER / MODIFIER
        # ====================================================

        self.bouton_enregistrer = Button(
            text="✓ ENREGISTRER",
            font_size="19sp",
            bold=True,
            size_hint_y=None,
            height=dp(62),
            background_normal="",
            background_color=VERT,
            color=BLANC
        )

        self.bouton_enregistrer.bind(
            on_press=self.enregistrer
        )

        contenu.add_widget(
            self.bouton_enregistrer
        )


        # ====================================================
        # ANNULER MODIFICATION
        # ====================================================

        self.bouton_annuler = Button(
            text="✕ ANNULER LA MODIFICATION",
            font_size="17sp",
            bold=True,
            size_hint_y=None,
            height=dp(55),
            background_normal="",
            background_color=ORANGE,
            color=BLANC
        )

        self.bouton_annuler.bind(
            on_press=self.annuler_modification
        )

        self.bouton_annuler.opacity = 0
        self.bouton_annuler.disabled = True

        contenu.add_widget(
            self.bouton_annuler
        )


        # ====================================================
        # HISTORIQUE
        # ====================================================

        historique = Button(
            text="📋 HISTORIQUE DES ÉCHOGRAPHIES",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(60),
            background_normal="",
            background_color=BLEU,
            color=BLANC
        )

        historique.bind(
            on_press=self.afficher_historique
        )

        contenu.add_widget(historique)


        scroll.add_widget(contenu)

        self.add_widget(scroll)


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
    # CHOISIR PATIENT
    # ========================================================

    def choisir_patient(self, instance):

        try:

            connexion = self.connexion()
            curseur = connexion.cursor()

            curseur.execute("""
                SELECT id, nom, prenom, age, sexe
                FROM patients
                ORDER BY id DESC
            """)

            patients = curseur.fetchall()

            connexion.close()

        except Exception as erreur:

            print(
                "ERREUR PATIENT :",
                erreur
            )

            self.message.text = (
                "Erreur lors du chargement des patients."
            )

            self.message.color = ROUGE

            return


        zone = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10)
        )

        scroll = ScrollView(
            do_scroll_x=False
        )

        liste = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None
        )

        liste.bind(
            minimum_height=liste.setter("height")
        )


        if not patients:

            liste.add_widget(
                Label(
                    text="Aucun patient enregistré.",
                    font_size="18sp",
                    size_hint_y=None,
                    height=dp(70)
                )
            )

        else:

            for patient in patients:

                texte = (
                    str(patient[1])
                    + " "
                    + str(patient[2] or "")
                    + "\nÂge : "
                    + str(patient[3] or "")
                    + "    Sexe : "
                    + str(patient[4] or "")
                )

                bouton = Button(
                    text=texte,
                    font_size="16sp",
                    size_hint_y=None,
                    height=dp(75),
                    background_normal="",
                    background_color=GRIS,
                    color=BLEU_FONCE
                )

                bouton.bind(
                    on_press=lambda btn, p=patient:
                    self.patient_selectionne(
                        p,
                        popup
                    )
                )

                liste.add_widget(bouton)


        scroll.add_widget(liste)
        zone.add_widget(scroll)


        fermer = Button(
            text="FERMER",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(55),
            background_normal="",
            background_color=BLEU_FONCE,
            color=BLANC
        )

        zone.add_widget(fermer)


        popup = Popup(
            title="PATIENTS",
            content=zone,
            size_hint=(0.95, 0.90)
        )

        fermer.bind(
            on_press=popup.dismiss
        )

        popup.open()


    # ========================================================
    # PATIENT SÉLECTIONNÉ
    # ========================================================

    def patient_selectionne(self, patient, popup):

        self.patient_id = patient[0]

        nom = patient[1] or ""
        prenom = patient[2] or ""

        self.patient.text = (
            "Patient : "
            + nom
            + " "
            + prenom
        )

        self.patient.color = VERT

        popup.dismiss()


    # ========================================================
    # ENREGISTRER / MODIFIER
    # ========================================================

    def enregistrer(self, instance):

        # ----------------------------------------------------
        # Vérifications
        # ----------------------------------------------------

        if self.patient_id is None:

            self.message.text = (
                "Veuillez choisir un patient."
            )

            self.message.color = ROUGE

            return


        if self.type_echo.text == "Choisir le type":

            self.message.text = (
                "Veuillez choisir le type d'échographie."
            )

            self.message.color = ROUGE

            return


        prix = self.prix.text.strip()

        if prix == "":
            prix = "0"


        try:

            montant = float(prix)

        except ValueError:

            self.message.text = (
                "Le prix est incorrect."
            )

            self.message.color = ROUGE

            return


        if montant < 0:

            self.message.text = (
                "Le prix ne peut pas être négatif."
            )

            self.message.color = ROUGE

            return


        connexion = None


        try:

            self.creer_table()
            self.preparer_caisse()

            connexion = self.connexion()
            curseur = connexion.cursor()


            # =================================================
            # MODIFICATION
            # =================================================

            if self.examen_id_modification is not None:

                examen_id = self.examen_id_modification


                curseur.execute(
                    """
                    UPDATE echographies
                    SET
                        patient_id = ?,
                        type_echographie = ?,
                        motif = ?,
                        observations = ?,
                        conclusion = ?,
                        prix = ?
                    WHERE id = ?
                    """,
                    (
                        self.patient_id,
                        self.type_echo.text,
                        self.motif.text.strip(),
                        self.observations.text.strip(),
                        self.conclusion.text.strip(),
                        prix,
                        examen_id
                    )
                )


                # ------------------------------------------------
                # Récupérer nom/prénom du patient
                # ------------------------------------------------

                curseur.execute(
                    """
                    SELECT nom, prenom
                    FROM patients
                    WHERE id = ?
                    """,
                    (
                        self.patient_id,
                    )
                )

                patient = curseur.fetchone()


                nom = ""
                prenom = ""


                if patient:

                    nom = patient[0] or ""
                    prenom = patient[1] or ""


                description = (
                    "Échographie "
                    + self.type_echo.text
                    + " - "
                    + nom
                    + " "
                    + prenom
                )


                date_operation = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )


                # ------------------------------------------------
                # Modifier recette caisse
                # ------------------------------------------------

                curseur.execute(
                    """
                    SELECT id
                    FROM caisse
                    WHERE echographie_id = ?
                    """,
                    (
                        examen_id,
                    )
                )

                operation = curseur.fetchone()


                if operation:

                    curseur.execute(
                        """
                        UPDATE caisse
                        SET
                            description = ?,
                            montant = ?,
                            type = 'Recette',
                            date_operation = ?
                        WHERE echographie_id = ?
                        """,
                        (
                            description,
                            montant,
                            date_operation,
                            examen_id
                        )
                    )

                elif montant > 0:

                    curseur.execute(
                        """
                        INSERT INTO caisse
                        (
                            description,
                            montant,
                            type,
                            date_operation,
                            echographie_id
                        )
                        VALUES (?, ?, 'Recette', ?, ?)
                        """,
                        (
                            description,
                            montant,
                            date_operation,
                            examen_id
                        )
                    )


                connexion.commit()


                self.message.text = (
                    "✓ Échographie modifiée avec succès."
                )

                self.message.color = VERT


                self.annuler_modification(
                    None,
                    afficher_message=False
                )


            # =================================================
            # NOUVELLE ÉCHOGRAPHIE
            # =================================================

            else:

                date = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )


                curseur.execute(
                    """
                    INSERT INTO echographies
                    (
                        patient_id,
                        type_echographie,
                        motif,
                        observations,
                        conclusion,
                        prix,
                        date_examen
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        self.patient_id,
                        self.type_echo.text,
                        self.motif.text.strip(),
                        self.observations.text.strip(),
                        self.conclusion.text.strip(),
                        prix,
                        date
                    )
                )


                examen_id = curseur.lastrowid


                # ------------------------------------------------
                # Récupérer patient
                # ------------------------------------------------

                curseur.execute(
                    """
                    SELECT nom, prenom
                    FROM patients
                    WHERE id = ?
                    """,
                    (
                        self.patient_id,
                    )
                )

                patient = curseur.fetchone()


                nom = ""
                prenom = ""


                if patient:

                    nom = patient[0] or ""
                    prenom = patient[1] or ""


                description = (
                    "Échographie "
                    + self.type_echo.text
                    + " - "
                    + nom
                    + " "
                    + prenom
                )


                # ------------------------------------------------
                # Ajouter à la caisse seulement si prix > 0
                # ------------------------------------------------

                if montant > 0:

                    date_operation = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )


                    curseur.execute(
                        """
                        INSERT INTO caisse
                        (
                            description,
                            montant,
                            type,
                            date_operation,
                            echographie_id
                        )
                        VALUES (?, ?, 'Recette', ?, ?)
                        """,
                        (
                            description,
                            montant,
                            date_operation,
                            examen_id
                        )
                    )


                connexion.commit()


                self.message.text = (
                    "✓ Échographie enregistrée."
                )

                self.message.color = VERT


                self.nettoyer_formulaire()


        except Exception as erreur:

            print(
                "ERREUR ECHOGRAPHIE :",
                erreur
            )

            if connexion:

                try:
                    connexion.rollback()
                except:
                    pass


            self.message.text = (
                "Erreur : " + str(erreur)
            )

            self.message.color = ROUGE


        finally:

            if connexion:
                connexion.close()


    # ========================================================
    # NETTOYER FORMULAIRE
    # ========================================================

    def nettoyer_formulaire(self):

        self.examen_id_modification = None

        self.patient_id = None

        self.patient.text = (
            "Aucun patient sélectionné"
        )

        self.patient.color = ROUGE

        self.type_echo.text = (
            "Choisir le type"
        )

        self.motif.text = ""
        self.observations.text = ""
        self.conclusion.text = ""
        self.prix.text = ""

        self.bouton_enregistrer.text = (
            "✓ ENREGISTRER"
        )

        self.bouton_enregistrer.background_color = VERT

        self.bouton_annuler.opacity = 0
        self.bouton_annuler.disabled = True


    # ========================================================
    # ANNULER MODIFICATION
    # ========================================================

    def annuler_modification(
        self,
        instance=None,
        afficher_message=True
    ):

        self.nettoyer_formulaire()

        if afficher_message:

            self.message.text = (
                "Modification annulée."
            )

            self.message.color = BLEU_FONCE


    # ========================================================
    # HISTORIQUE
    # ========================================================

    def afficher_historique(self, instance):

        contenu = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(10)
        )


        recherche = TextInput(
            hint_text="🔎 Rechercher un patient par nom ou prénom...",
            font_size="17sp",
            multiline=False,
            size_hint_y=None,
            height=dp(52)
        )

        contenu.add_widget(recherche)


        scroll = ScrollView(
            do_scroll_x=False
        )


        liste = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None
        )

        liste.bind(
            minimum_height=liste.setter("height")
        )


        scroll.add_widget(liste)

        contenu.add_widget(scroll)


        fermer = Button(
            text="FERMER",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=dp(52),
            background_normal="",
            background_color=BLEU_FONCE,
            color=BLANC
        )

        contenu.add_widget(fermer)


        popup = Popup(
            title="HISTORIQUE DES ÉCHOGRAPHIES",
            content=contenu,
            size_hint=(0.96, 0.90)
        )


        fermer.bind(
            on_press=popup.dismiss
        )


        # ====================================================
        # CHARGER HISTORIQUE
        # ====================================================

        def charger_historique(
            texte_recherche=""
        ):

            liste.clear_widgets()

            connexion = None


            try:

                connexion = self.connexion()
                curseur = connexion.cursor()

                recherche_texte = (
                    texte_recherche.strip()
                )


                if recherche_texte:

                    mot = (
                        "%"
                        + recherche_texte
                        + "%"
                    )


                    curseur.execute(
                        """
                        SELECT
                            e.id,
                            e.patient_id,
                            p.nom,
                            p.prenom,
                            e.type_echographie,
                            e.prix,
                            e.date_examen
                        FROM echographies e
                        LEFT JOIN patients p
                            ON e.patient_id = p.id
                        WHERE
                            p.nom LIKE ?
                            OR p.prenom LIKE ?
                            OR (p.nom || ' ' || p.prenom) LIKE ?
                            OR (p.prenom || ' ' || p.nom) LIKE ?
                        ORDER BY e.id DESC
                        """,
                        (
                            mot,
                            mot,
                            mot,
                            mot
                        )
                    )

                else:

                    curseur.execute(
                        """
                        SELECT
                            e.id,
                            e.patient_id,
                            p.nom,
                            p.prenom,
                            e.type_echographie,
                            e.prix,
                            e.date_examen
                        FROM echographies e
                        LEFT JOIN patients p
                            ON e.patient_id = p.id
                        ORDER BY e.id DESC
                        """
                    )


                examens = curseur.fetchall()


            except Exception as erreur:

                examens = []

                print(
                    "ERREUR HISTORIQUE :",
                    erreur
                )


            finally:

                if connexion:
                    connexion.close()


            # =================================================
            # AUCUN RÉSULTAT
            # =================================================

            if not examens:

                if recherche_texte:

                    message = (
                        "Aucune échographie trouvée\n"
                        "pour : "
                        + recherche_texte
                    )

                else:

                    message = (
                        "Aucune échographie enregistrée."
                    )


                liste.add_widget(
                    Label(
                        text=message,
                        font_size="18sp",
                        color=BLEU_FONCE,
                        size_hint_y=None,
                        height=dp(80),
                        halign="center",
                        valign="middle"
                    )
                )

                return


            # =================================================
            # AFFICHER
            # =================================================

            for examen in examens:

                examen_id = examen[0]

                nom = examen[2] or ""
                prenom = examen[3] or ""

                type_echo = examen[4] or ""
                prix = examen[5] or "0"
                date = examen[6] or ""


                texte = (
                    "ÉCHOGRAPHIE N° "
                    + str(examen_id)
                    + "\n"
                    + "Patient : "
                    + nom
                    + " "
                    + prenom
                    + "\n"
                    + type_echo
                    + "  •  "
                    + str(prix)
                    + " FCFA\n"
                    + date
                )


                ligne = BoxLayout(
                    orientation="vertical",
                    spacing=dp(5),
                    padding=dp(8),
                    size_hint_y=None,
                    height=dp(185)
                )


                label = Label(
                    text=texte,
                    font_size="15sp",
                    color=BLEU_FONCE,
                    halign="left",
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


                boutons = BoxLayout(
                    spacing=dp(6),
                    size_hint_y=None,
                    height=dp(42)
                )


                voir = Button(
                    text="VOIR",
                    font_size="14sp",
                    bold=True,
                    background_normal="",
                    background_color=BLEU,
                    color=BLANC
                )


                modifier = Button(
                    text="✏️ MODIFIER",
                    font_size="14sp",
                    bold=True,
                    background_normal="",
                    background_color=ORANGE,
                    color=BLANC
                )


                supprimer = Button(
                    text="🗑️ SUPPRIMER",
                    font_size="14sp",
                    bold=True,
                    background_normal="",
                    background_color=ROUGE,
                    color=BLANC
                )


                voir.bind(
                    on_press=lambda btn,
                    eid=examen_id:
                    self.voir_echographie(eid)
                )


                modifier.bind(
                    on_press=lambda btn,
                    eid=examen_id:
                    self.modifier_echographie(
                        eid,
                        popup
                    )
                )


                supprimer.bind(
                    on_press=lambda btn,
                    eid=examen_id:
                    self.confirmer_suppression(
                        eid,
                        popup
                    )
                )


                boutons.add_widget(voir)
                boutons.add_widget(modifier)
                boutons.add_widget(supprimer)


                ligne.add_widget(label)
                ligne.add_widget(boutons)


                liste.add_widget(ligne)


        recherche.bind(
            text=lambda instance, value:
            charger_historique(value)
        )


        charger_historique()

        popup.open()


    # ========================================================
    # MODIFIER UNE ÉCHOGRAPHIE
    # ========================================================

    def modifier_echographie(
        self,
        examen_id,
        popup_historique=None
    ):

        connexion = None


        try:

            connexion = self.connexion()
            curseur = connexion.cursor()


            curseur.execute(
                """
                SELECT
                    e.id,
                    e.patient_id,
                    p.nom,
                    p.prenom,
                    e.type_echographie,
                    e.motif,
                    e.observations,
                    e.conclusion,
                    e.prix
                FROM echographies e
                LEFT JOIN patients p
                    ON e.patient_id = p.id
                WHERE e.id = ?
                """,
                (
                    examen_id,
                )
            )


            examen = curseur.fetchone()


        except Exception as erreur:

            print(
                "ERREUR MODIFICATION :",
                erreur
            )

            examen = None


        finally:

            if connexion:
                connexion.close()


        if not examen:

            return


        # ----------------------------------------------------
        # Charger les données
        # ----------------------------------------------------

        self.examen_id_modification = examen[0]

        self.patient_id = examen[1]


        nom = examen[2] or ""
        prenom = examen[3] or ""


        self.patient.text = (
            "Patient : "
            + nom
            + " "
            + prenom
        )

        self.patient.color = VERT


        self.type_echo.text = (
            examen[4]
            or "Choisir le type"
        )


        self.motif.text = (
            examen[5]
            or ""
        )


        self.observations.text = (
            examen[6]
            or ""
        )


        self.conclusion.text = (
            examen[7]
            or ""
        )


        prix = examen[8]

        if prix is None:
            prix = ""

        self.prix.text = str(prix)


        # ----------------------------------------------------
        # Changer le bouton
        # ----------------------------------------------------

        self.bouton_enregistrer.text = (
            "✓ ENREGISTRER LES MODIFICATIONS"
        )

        self.bouton_enregistrer.background_color = (
            ORANGE
        )


        self.bouton_annuler.opacity = 1
        self.bouton_annuler.disabled = False


        self.message.text = (
            "Mode modification activé."
        )

        self.message.color = ORANGE


        if popup_historique:

            popup_historique.dismiss()


    # ========================================================
    # VOIR UNE ÉCHOGRAPHIE
    # ========================================================

    def voir_echographie(
        self,
        examen_id
    ):

        connexion = None


        try:

            connexion = self.connexion()
            curseur = connexion.cursor()


            curseur.execute(
                """
                SELECT
                    e.id,
                    p.nom,
                    p.prenom,
                    e.type_echographie,
                    e.motif,
                    e.observations,
                    e.conclusion,
                    e.prix,
                    e.date_examen
                FROM echographies e
                LEFT JOIN patients p
                    ON e.patient_id = p.id
                WHERE e.id = ?
                """,
                (
                    examen_id,
                )
            )


            examen = curseur.fetchone()


        except Exception as erreur:

            print(
                "ERREUR DÉTAIL :",
                erreur
            )

            examen = None


        finally:

            if connexion:
                connexion.close()


        if not examen:

            return


        texte = (
            "ECHOGRAPHIE NAYE\n"
            "============================\n\n"
            "ÉCHOGRAPHIE N° "
            + str(examen[0])
            + "\n\n"
            "PATIENT : "
            + str(examen[1] or "")
            + " "
            + str(examen[2] or "")
            + "\n\n"
            "TYPE : "
            + str(examen[3] or "")
            + "\n\n"
            "MOTIF :\n"
            + str(examen[4] or "")
            + "\n\n"
            "OBSERVATIONS :\n"
            + str(examen[5] or "")
            + "\n\n"
            "CONCLUSION :\n"
            + str(examen[6] or "")
            + "\n\n"
            "PRIX : "
            + str(examen[7] or "0")
            + " FCFA\n\n"
            "DATE : "
            + str(examen[8] or "")
        )


        self.afficher_message(
            "DÉTAIL DE L'ÉCHOGRAPHIE",
            texte
        )


    # ========================================================
    # CONFIRMATION SUPPRESSION
    # ========================================================

    def confirmer_suppression(
        self,
        examen_id,
        popup_historique
    ):

        contenu = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(15)
        )


        texte = Label(
            text=(
                "Voulez-vous vraiment supprimer\n"
                "cette échographie ?\n\n"
                "Le paiement associé sera également supprimé."
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
            size_hint=(0.90, 0.45),
            auto_dismiss=False
        )


        annuler.bind(
            on_press=popup_confirmation.dismiss
        )


        supprimer.bind(
            on_press=lambda btn:
            self.supprimer_echographie(
                examen_id,
                popup_confirmation,
                popup_historique
            )
        )


        popup_confirmation.open()


    # ========================================================
    # SUPPRIMER ECHOGRAPHIE + CAISSE
    # ========================================================

    def supprimer_echographie(
        self,
        examen_id,
        popup_confirmation,
        popup_historique
    ):

        connexion = None


        try:

            connexion = self.connexion()
            curseur = connexion.cursor()


            # ------------------------------------------------
            # Supprimer le paiement lié
            # ------------------------------------------------

            curseur.execute(
                """
                DELETE FROM caisse
                WHERE echographie_id = ?
                """,
                (
                    examen_id,
                )
            )


            # ------------------------------------------------
            # Supprimer l'échographie
            # ------------------------------------------------

            curseur.execute(
                """
                DELETE FROM echographies
                WHERE id = ?
                """,
                (
                    examen_id,
                )
            )


            connexion.commit()


            popup_confirmation.dismiss()
            popup_historique.dismiss()


            self.message.text = (
                "✓ Échographie et paiement supprimés."
            )

            self.message.color = VERT


        except Exception as erreur:

            print(
                "ERREUR SUPPRESSION :",
                erreur
            )


            if connexion:

                try:
                    connexion.rollback()
                except:
                    pass


            popup_confirmation.dismiss()


            self.message.text = (
                "Erreur lors de la suppression."
            )

            self.message.color = ROUGE


        finally:

            if connexion:
                connexion.close()


    # ========================================================
    # MESSAGE
    # ========================================================

    def afficher_message(
        self,
        titre,
        texte
    ):

        contenu = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(12)
        )


        label = Label(
            text=texte,
            font_size="15sp",
            color=GRIS_FONCE,
            halign="left",
            valign="top"
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


        fermer = Button(
            text="FERMER",
            font_size="17sp",
            bold=True,
            size_hint_y=None,
            height=dp(50),
            background_normal="",
            background_color=BLEU_FONCE,
            color=BLANC
        )


        contenu.add_widget(fermer)


        popup = Popup(
            title=titre,
            content=contenu,
            size_hint=(0.94, 0.82)
        )


        fermer.bind(
            on_press=popup.dismiss
        )


        popup.open()


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


    class EchographieApp(App):

        def build(self):

            return EchographieScreen(self)


    EchographieApp().run()