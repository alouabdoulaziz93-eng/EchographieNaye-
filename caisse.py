import sqlite3
from datetime import datetime

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
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
GRIS = (0.95, 0.95, 0.95, 1)
GRIS_FONCE = (0.25, 0.25, 0.25, 1)
BLANC = (1, 1, 1, 1)


# ============================================================
# BOUTON
# ============================================================

class Bouton(Button):

    def __init__(self, couleur=BLEU, **kwargs):

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = couleur

        self.color = BLANC
        self.bold = True
        self.font_size = dp(15)


# ============================================================
# CAISSE
# ============================================================

class CaisseScreen(BoxLayout):

    def __init__(self, app, **kwargs):

        super().__init__(**kwargs)

        self.app = app

        self.orientation = "vertical"
        self.padding = dp(12)
        self.spacing = dp(8)

        self.creer_table()
        self.construire_interface()


    # ========================================================
    # CONNEXION
    # ========================================================

    def connexion(self):

        return sqlite3.connect(DB_NAME)


    # ========================================================
    # CRÉATION / MISE À JOUR TABLE
    # ========================================================

    def creer_table(self):

        conn = None

        try:

            conn = self.connexion()
            cursor = conn.cursor()

            # Table principale
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS caisse (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    montant REAL DEFAULT 0,
                    type TEXT NOT NULL,
                    date_operation TEXT,
                    echographie_id INTEGER
                )
            """)

            # ------------------------------------------------
            # Vérifier les anciennes colonnes
            # ------------------------------------------------

            cursor.execute(
                "PRAGMA table_info(caisse)"
            )

            colonnes = [
                ligne[1]
                for ligne in cursor.fetchall()
            ]

            # ------------------------------------------------
            # Ajouter echographie_id si elle n'existe pas
            # ------------------------------------------------

            if "echographie_id" not in colonnes:

                cursor.execute("""
                    ALTER TABLE caisse
                    ADD COLUMN echographie_id INTEGER
                """)

            conn.commit()

        except Exception as erreur:

            print(
                "ERREUR CREATION / MISE À JOUR CAISSE :",
                erreur
            )

        finally:

            if conn:
                conn.close()


    # ========================================================
    # AJOUTER AUTOMATIQUEMENT UNE ÉCHOGRAPHIE À LA CAISSE
    # ========================================================

    def ajouter_recette_echographie(
        self,
        echographie_id,
        description,
        montant
    ):

        """
        Ajoute automatiquement une échographie
        dans la caisse.

        echographie_id :
            ID de l'échographie

        description :
            Exemple :
            Échographie Obstétricale - AMIRA

        montant :
            Montant en FCFA
        """

        conn = None

        try:

            self.creer_table()

            montant = float(montant)

            if montant <= 0:
                return False

            conn = self.connexion()
            cursor = conn.cursor()

            # ------------------------------------------------
            # Vérifier si cette échographie est déjà dans caisse
            # ------------------------------------------------

            cursor.execute("""
                SELECT id
                FROM caisse
                WHERE echographie_id = ?
            """, (echographie_id,))

            operation = cursor.fetchone()

            date_operation = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # ------------------------------------------------
            # SI ELLE EXISTE → MODIFIER
            # ------------------------------------------------

            if operation:

                cursor.execute("""
                    UPDATE caisse
                    SET
                        description = ?,
                        montant = ?,
                        type = 'Recette',
                        date_operation = ?
                    WHERE echographie_id = ?
                """, (
                    description,
                    montant,
                    date_operation,
                    echographie_id
                ))

            # ------------------------------------------------
            # SINON → CRÉER
            # ------------------------------------------------

            else:

                cursor.execute("""
                    INSERT INTO caisse
                    (
                        description,
                        montant,
                        type,
                        date_operation,
                        echographie_id
                    )
                    VALUES (?, ?, 'Recette', ?, ?)
                """, (
                    description,
                    montant,
                    date_operation,
                    echographie_id
                ))

            conn.commit()

            return True

        except Exception as erreur:

            print(
                "ERREUR AJOUT ECHOGRAPHIE CAISSE :",
                erreur
            )

            return False

        finally:

            if conn:
                conn.close()


    # ========================================================
    # MODIFIER LE PAIEMENT D'UNE ÉCHOGRAPHIE
    # ========================================================

    def modifier_recette_echographie(
        self,
        echographie_id,
        description,
        montant
    ):

        return self.ajouter_recette_echographie(
            echographie_id,
            description,
            montant
        )


    # ========================================================
    # SUPPRIMER LE PAIEMENT D'UNE ÉCHOGRAPHIE
    # ========================================================

    def supprimer_recette_echographie(
        self,
        echographie_id
    ):

        conn = None

        try:

            conn = self.connexion()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM caisse
                WHERE echographie_id = ?
            """, (
                echographie_id,
            ))

            conn.commit()

            return True

        except Exception as erreur:

            print(
                "ERREUR SUPPRESSION PAIEMENT ECHOGRAPHIE :",
                erreur
            )

            return False

        finally:

            if conn:
                conn.close()


    # ========================================================
    # INTERFACE
    # ========================================================

    def construire_interface(self):

        titre = Label(
            text="💰 CAISSE",
            font_size="28sp",
            bold=True,
            color=BLEU_FONCE,
            size_hint_y=None,
            height=dp(60)
        )

        self.add_widget(titre)


        # ----------------------------------------------------
        # TOTAL
        # ----------------------------------------------------

        self.total_label = Label(
            text="TOTAL ENCAISSÉ : 0 FCFA",
            font_size="21sp",
            bold=True,
            color=VERT,
            size_hint_y=None,
            height=dp(55)
        )

        self.add_widget(self.total_label)

        self.actualiser_total()


        # ----------------------------------------------------
        # FORMULAIRE
        # ----------------------------------------------------

        formulaire = GridLayout(
            cols=1,
            spacing=dp(7),
            size_hint_y=None
        )

        formulaire.bind(
            minimum_height=formulaire.setter("height")
        )


        # DESCRIPTION

        formulaire.add_widget(
            Label(
                text="DESCRIPTION",
                font_size="17sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(35)
            )
        )


        self.description = TextInput(
            hint_text="Exemple : Échographie obstétricale",
            font_size="17sp",
            multiline=False,
            size_hint_y=None,
            height=dp(52)
        )

        formulaire.add_widget(
            self.description
        )


        # MONTANT

        formulaire.add_widget(
            Label(
                text="MONTANT (FCFA)",
                font_size="17sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(35)
            )
        )


        self.montant = TextInput(
            hint_text="Exemple : 15000",
            font_size="17sp",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(52)
        )

        formulaire.add_widget(
            self.montant
        )


        # TYPE

        formulaire.add_widget(
            Label(
                text="TYPE D'OPÉRATION",
                font_size="17sp",
                bold=True,
                color=BLEU_FONCE,
                size_hint_y=None,
                height=dp(35)
            )
        )


        from kivy.uix.spinner import Spinner

        self.type_operation = Spinner(
            text="Recette",
            values=(
                "Recette",
                "Dépense"
            ),
            font_size="17sp",
            size_hint_y=None,
            height=dp(52)
        )

        formulaire.add_widget(
            self.type_operation
        )


        # BOUTON ENREGISTRER

        enregistrer = Bouton(
            text="✓ ENREGISTRER",
            couleur=VERT,
            size_hint_y=None,
            height=dp(58)
        )

        enregistrer.bind(
            on_release=self.enregistrer
        )

        formulaire.add_widget(
            enregistrer
        )


        # MESSAGE

        self.message = Label(
            text="",
            font_size="15sp",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )

        formulaire.add_widget(
            self.message
        )


        self.add_widget(
            formulaire
        )


        # ----------------------------------------------------
        # HISTORIQUE
        # ----------------------------------------------------

        historique_titre = Label(
            text="📋 HISTORIQUE DES OPÉRATIONS",
            font_size="19sp",
            bold=True,
            color=BLEU_FONCE,
            size_hint_y=None,
            height=dp(45)
        )

        self.add_widget(
            historique_titre
        )


        self.scroll = ScrollView(
            do_scroll_x=False
        )


        self.liste = GridLayout(
            cols=1,
            spacing=dp(7),
            size_hint_y=None
        )

        self.liste.bind(
            minimum_height=self.liste.setter("height")
        )


        self.scroll.add_widget(
            self.liste
        )

        self.add_widget(
            self.scroll
        )


        self.actualiser_historique()


        # ----------------------------------------------------
        # RETOUR
        # ----------------------------------------------------

        retour = Bouton(
            text="← RETOUR AU MENU",
            couleur=BLEU_FONCE,
            size_hint_y=None,
            height=dp(58)
        )

        retour.bind(
            on_release=self.retour
        )

        self.add_widget(
            retour
        )


    # ========================================================
    # ENREGISTRER OPÉRATION MANUELLE
    # ========================================================

    def enregistrer(self, instance):

        description = self.description.text.strip()
        montant_text = self.montant.text.strip()
        type_operation = self.type_operation.text


        if not description:

            self.message.text = (
                "Veuillez entrer une description."
            )

            self.message.color = ROUGE

            return


        if not montant_text:

            self.message.text = (
                "Veuillez entrer le montant."
            )

            self.message.color = ROUGE

            return


        try:

            montant = float(montant_text)

        except ValueError:

            self.message.text = (
                "Montant incorrect."
            )

            self.message.color = ROUGE

            return


        if montant <= 0:

            self.message.text = (
                "Le montant doit être supérieur à 0."
            )

            self.message.color = ROUGE

            return


        conn = None

        try:

            conn = self.connexion()
            cursor = conn.cursor()

            date_operation = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )


            cursor.execute(
                """
                INSERT INTO caisse
                (
                    description,
                    montant,
                    type,
                    date_operation,
                    echographie_id
                )
                VALUES (?, ?, ?, ?, NULL)
                """,
                (
                    description,
                    montant,
                    type_operation,
                    date_operation
                )
            )


            conn.commit()


            self.description.text = ""
            self.montant.text = ""


            self.message.text = (
                "✓ Opération enregistrée."
            )

            self.message.color = VERT


            self.actualiser_total()
            self.actualiser_historique()


        except Exception as erreur:

            print(
                "ERREUR CAISSE :",
                erreur
            )

            self.message.text = (
                "Erreur lors de l'enregistrement."
            )

            self.message.color = ROUGE

        finally:

            if conn:
                conn.close()


    # ========================================================
    # TOTAL
    # ========================================================

    def actualiser_total(self):

        try:

            conn = self.connexion()
            cursor = conn.cursor()


            cursor.execute("""
                SELECT
                    COALESCE(
                        SUM(
                            CASE
                                WHEN type = 'Recette'
                                THEN montant
                                ELSE -montant
                            END
                        ),
                        0
                    )
                FROM caisse
            """)


            total = cursor.fetchone()[0] or 0

            conn.close()


            self.total_label.text = (
                "TOTAL CAISSE : "
                + self.format_fcfa(total)
            )


        except Exception as erreur:

            print(
                "ERREUR TOTAL :",
                erreur
            )


    # ========================================================
    # HISTORIQUE
    # ========================================================

    def actualiser_historique(self):

        self.liste.clear_widgets()


        try:

            conn = self.connexion()
            cursor = conn.cursor()


            cursor.execute("""
                SELECT
                    id,
                    description,
                    montant,
                    type,
                    date_operation,
                    echographie_id
                FROM caisse
                ORDER BY id DESC
            """)


            operations = cursor.fetchall()

            conn.close()


        except Exception as erreur:

            print(
                "ERREUR HISTORIQUE :",
                erreur
            )

            return


        if not operations:

            self.liste.add_widget(
                Label(
                    text="Aucune opération enregistrée.",
                    font_size="16sp",
                    color=GRIS_FONCE,
                    size_hint_y=None,
                    height=dp(55)
                )
            )

            return


        for operation in operations:

            identifiant = operation[0]
            description = operation[1]
            montant = operation[2] or 0
            type_operation = operation[3]
            date_operation = operation[4]
            echographie_id = operation[5]


            carte = BoxLayout(
                orientation="vertical",
                spacing=dp(3),
                padding=dp(8),
                size_hint_y=None,
                height=dp(120)
            )


            texte = (
                f"N° {identifiant}  •  "
                f"{type_operation}\n"
                f"{description}\n"
                f"Montant : "
                f"{self.format_fcfa(montant)}\n"
                f"{date_operation}"
            )


            if echographie_id:

                texte += (
                    "\n🩻 Paiement échographie N° "
                    + str(echographie_id)
                )


            label = Label(
                text=texte,
                font_size="14sp",
                color=GRIS_FONCE,
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


            supprimer = Bouton(
                text="🗑 SUPPRIMER",
                couleur=ROUGE,
                size_hint_y=None,
                height=dp(35)
            )


            supprimer.bind(
                on_release=lambda btn,
                op=operation:
                self.confirmer_suppression(op)
            )


            carte.add_widget(label)
            carte.add_widget(supprimer)


            self.liste.add_widget(
                carte
            )


    # ========================================================
    # CONFIRMATION SUPPRESSION
    # ========================================================

    def confirmer_suppression(self, operation):

        identifiant = operation[0]
        echographie_id = operation[5]


        contenu = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(12)
        )


        message = (
            "Voulez-vous vraiment supprimer\n"
            f"l'opération N° {identifiant} ?"
        )


        if echographie_id:

            message += (
                "\n\n⚠️ Cette opération est liée "
                "à une échographie."
            )


        label = Label(
            text=message,
            font_size="16sp",
            color=GRIS_FONCE,
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


        boutons = BoxLayout(
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )


        oui = Bouton(
            text="OUI, SUPPRIMER",
            couleur=ROUGE
        )


        non = Bouton(
            text="ANNULER",
            couleur=BLEU_FONCE
        )


        boutons.add_widget(oui)
        boutons.add_widget(non)


        contenu.add_widget(label)
        contenu.add_widget(boutons)


        popup = Popup(
            title="CONFIRMATION",
            content=contenu,
            size_hint=(0.90, 0.45),
            auto_dismiss=False
        )


        oui.bind(
            on_release=lambda btn:
            self.supprimer_operation(
                identifiant,
                popup
            )
        )


        non.bind(
            on_release=popup.dismiss
        )


        popup.open()


    # ========================================================
    # SUPPRIMER OPÉRATION
    # ========================================================

    def supprimer_operation(
        self,
        identifiant,
        popup
    ):

        try:

            conn = self.connexion()
            cursor = conn.cursor()


            cursor.execute(
                """
                DELETE FROM caisse
                WHERE id = ?
                """,
                (identifiant,)
            )


            conn.commit()
            conn.close()


            popup.dismiss()


            self.actualiser_total()
            self.actualiser_historique()


            self.message.text = (
                "✓ Opération supprimée."
            )

            self.message.color = VERT


        except Exception as erreur:

            print(
                "ERREUR SUPPRESSION :",
                erreur
            )


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
    # RETOUR
    # ========================================================

    def retour(self, instance):

        self.app.afficher_menu()


# ============================================================
# TEST DIRECT
# ============================================================

if __name__ == "__main__":

    from kivy.app import App


    class CaisseApp(App):

        def build(self):

            return CaisseScreen(self)


    CaisseApp().run()