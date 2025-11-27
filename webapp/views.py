import calendar

from flask_appbuilder import ModelView
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface

from . import appbuilder, db
from flask import render_template
from flask_appbuilder import BaseView, expose

class DomovView(BaseView):
    route_base = "/"

    @expose("/")
    def index(self):
        return """
        <div style="padding: 40px; font-family: Arial;">
            <h1 style="color: #0066cc;">🔷 DataHub Manager Pro</h1>
            <p style="font-size: 18px; color: #555;">
                Centralizovaná platforma pro správu podnikových dat, 
                zásobování a kompletní evidenci obchodních partnerů
            </p>
            <hr style="border: 1px solid #ddd;">
            <h3>Funkce systému:</h3>
            <ul style="line-height: 2;">
                <li>📦 Správa skladových položek a zásob</li>
                <li>👥 Evidence partnerů a zákazníků</li>
                <li>📊 Statistické přehledy a grafy</li>
                <li>🔐 Pokročilé zabezpečení dat</li>
            </ul>
        </div>
        """

appbuilder.add_view_no_menu(DomovView)

class InfoView(BaseView):
    route_base = "/info"

    @expose("/")
    def index(self):
        return """
        <div style="padding: 30px; font-family: Arial; background: #f5f5f5; border-radius: 8px;">
            <h2 style="color: #0066cc;">ℹ️ O platformě DataHub Manager Pro</h2>
            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                <tr style="background: #e0e0e0;">
                    <td style="padding: 10px; font-weight: bold;">Verze</td>
                    <td style="padding: 10px;">3.5.1 Enterprise Edition</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold;">Vývojový tým</td>
                    <td style="padding: 10px;">DataHub Solutions Team</td>
                </tr>
                <tr style="background: #e0e0e0;">
                    <td style="padding: 10px; font-weight: bold;">Licence</td>
                    <td style="padding: 10px;">Commercial Pro License 2025</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold;">Účel</td>
                    <td style="padding: 10px;">Komplexní řešení pro správu podnikových dat, skladu a CRM</td>
                </tr>
                <tr style="background: #e0e0e0;">
                    <td style="padding: 10px; font-weight: bold;">Podpora</td>
                    <td style="padding: 10px;">support@datahub-solutions.com</td>
                </tr>
            </table>
            <p style="margin-top: 20px; color: #666;">
                © 2025 DataHub Solutions. Všechna práva vyhrazena.
            </p>
        </div>
        """

appbuilder.add_view(InfoView, "O Platformě", icon="fa-info-circle", category="Nápověda")

from webapp.models import Zakaznik, Kategorie, Typ, Polozka, Zasoba

def inicializovat_typy():
    try:
        db.session.add(Typ(oznaceni="Typ A"))
        db.session.add(Typ(oznaceni="Typ B"))
        db.session.commit()
    except Exception:
        db.session.rollback()


class PolozkaSeznamView(ModelView):
    datamodel = SQLAInterface(Polozka)
    list_columns = ["nazev", "kod", "cena"]
    label_columns = {"nazev": "Název položky", "kod": "Kód", "cena": "Cena"}

class ZasobaSeznamView(ModelView):
    datamodel = SQLAInterface(Zasoba)
    list_columns = ["nazev", "datum_pridani", "pocet", "aktivni"]
    label_columns = {"nazev": "Název", "datum_pridani": "Datum přidání", "pocet": "Počet kusů", "aktivni": "Aktivní"}

appbuilder.add_view(
    PolozkaSeznamView, "Katalog Produktů", icon="fa-shopping-cart", category="Warehouse Management"
)

appbuilder.add_view(
    ZasobaSeznamView, "Stav Skladu", icon="fa-database", category="Warehouse Management"
)    

class ZakaznikSeznamView(ModelView):
    datamodel = SQLAInterface(Zakaznik)

    list_columns = ["jmeno", "telefon_mobil", "datum_narozeni", "kategorie.oznaceni"]
    label_columns = {
        "jmeno": "Jméno partnera", 
        "telefon_mobil": "Telefon", 
        "datum_narozeni": "Datum narození",
        "kategorie.oznaceni": "Segment"
    }

    base_order = ("jmeno", "asc")
    show_fieldsets = [
        ("Profil partnera", {"fields": ["jmeno", "typ", "kategorie"]}),
        (
            "Kontaktní údaje",
            {
                "fields": [
                    "adresa",
                    "datum_narozeni",
                    "telefon_pevny",
                    "telefon_mobil",
                ],
                "expanded": False,
            },
        ),
    ]

    add_fieldsets = [
        ("Profil partnera", {"fields": ["jmeno", "typ", "kategorie"]}),
        (
            "Kontaktní údaje",
            {
                "fields": [
                    "adresa",
                    "datum_narozeni",
                    "telefon_pevny",
                    "telefon_mobil",
                ],
                "expanded": False,
            },
        ),
    ]

    edit_fieldsets = [
        ("Profil partnera", {"fields": ["jmeno", "typ", "kategorie"]}),
        (
            "Kontaktní údaje",
            {
                "fields": [
                    "adresa",
                    "datum_narozeni",
                    "telefon_pevny",
                    "telefon_mobil",
                ],
                "expanded": False,
            },
        ),
    ]


class KategorieSeznamView(ModelView):
    datamodel = SQLAInterface(Kategorie)
    related_views = [ZakaznikSeznamView]
    label_columns = {"oznaceni": "Název segmentu"}


def formatovat_mesic_rok(hodnota):
    return calendar.month_name[hodnota.month] + " " + str(hodnota.year)


def formatovat_rok(hodnota):
    return str(hodnota.year)


class ZakaznikGrafView(GroupByChartView):
    datamodel = SQLAInterface(Zakaznik)

    chart_title = "Demografická analýza obchodních partnerů"
    chart_type = "ColumnChart"
    label_columns = ZakaznikSeznamView.label_columns
    definitions = [
        {
            "group": "mesic_rok",
            "formatter": formatovat_mesic_rok,
            "series": [(aggregate_count, "group")],
        },
        {
            "group": "rok",
            "formatter": formatovat_rok,
            "series": [(aggregate_count, "group")],
        },
    ]


db.create_all()
inicializovat_typy()
appbuilder.add_view(
    KategorieSeznamView,
    "Segmenty",
    icon="fa-bookmark",
    category="CRM Module",
    category_icon="fa-briefcase",
)
appbuilder.add_view(
    ZakaznikSeznamView, "Obchodní Partneři", icon="fa-handshake-o", category="CRM Module"
)
appbuilder.add_separator("CRM Module")
appbuilder.add_view(
    ZakaznikGrafView,
    "Analytics Dashboard",
    icon="fa-line-chart",
    category="CRM Module",
)
