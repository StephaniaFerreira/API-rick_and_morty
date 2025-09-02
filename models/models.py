from sqlalchemy import Column, Integer, String
from database import Base

class Personagem(Base):
    __tablename__ = 'Personagem'

    id_personagem = Column(Integer, primary_key=True)
    name = Column(String(50))
    status = Column(String(50))
    species = Column(String(50))
    gender = Column(String(50))
    location = Column(String(50))

class Dublador(Base):
    __tablename__ = 'Dublador'

    id_dublador = Column(Integer, primary_key=True)
    name = Column(String(50))
    character = Column(String(50))
    serie = Column(Integer)

class Episodio(Base):
    __tablename__ = 'Episodio'

    id_episodio = Column(Integer, primary_key=True)
    id_externo = Column(Integer)
    episode_number = Column(Integer)
    name = Column(String(50))
    overview = Column(String(200))
    runtime = Column(Integer)
    id_personagem = Column(Integer)
    season = Column(Integer)

