import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship

mindate = datetime.date(datetime.MINYEAR, 1, 1)


class Kategorie(Model):
    id = Column(Integer, primary_key=True)
    oznaceni = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.oznaceni


class Typ(Model):
    id = Column(Integer, primary_key=True)
    oznaceni = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.oznaceni


class Zakaznik(Model):
    id = Column(Integer, primary_key=True)
    jmeno = Column(String(150), unique=True, nullable=False)
    adresa = Column(String(564))
    datum_narozeni = Column(Date, nullable=True)
    telefon_pevny = Column(String(20))
    telefon_mobil = Column(String(20))
    kategorie_id = Column(Integer, ForeignKey("kategorie.id"), nullable=False)
    kategorie = relationship("Kategorie")
    typ_id = Column(Integer, ForeignKey("typ.id"), nullable=False)
    typ = relationship("Typ")

    def __repr__(self):
        return self.jmeno

    def mesic_rok(self):
        datum = self.datum_narozeni or mindate
        return datetime.datetime(datum.year, datum.month, 1) or mindate

    def rok(self):
        datum = self.datum_narozeni or mindate
        return datetime.datetime(datum.year, 1, 1)
    

class Polozka(Model):
    id = Column(Integer, primary_key=True)
    nazev = Column(String(64), unique=True, nullable=False)
    kod = Column(Integer, unique=True)
    cena = Column(Float, nullable=True)
    
    def __repr__(self):
        return self.nazev
    
class Zasoba(Model):
    id = Column(Integer, primary_key=True)
    nazev = Column(String(64), unique=True, nullable=False)
    datum_pridani = Column(Date, nullable=True)
    pocet = Column(Integer, nullable=True)
    aktivni = Column(Boolean, nullable=True)
    popis = Column(String(256))
    
    def __repr__(self):
        return self.nazev    
    



