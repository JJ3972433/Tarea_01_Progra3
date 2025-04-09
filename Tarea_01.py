from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

# Configuración base de datos
DATABASE_URL = "sqlite:///./misiones.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Tabla de relación entre personajes y misiones
personaje_misiones = Table(
    'personaje_misiones',
    Base.metadata,
    Column('personaje_id', Integer, ForeignKey('personajes.id')),
    Column('mision_id', Integer, ForeignKey('misiones.id'))
)

# Modelos ORM
class Personaje(Base):
    __tablename__ = 'personajes'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    xp = Column(Integer, default=0)
    misiones = relationship("Mision", secondary=personaje_misiones)

class Mision(Base):
    __tablename__ = 'misiones'
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    xp_recompensa = Column(Integer)

# Crear las tablas
Base.metadata.create_all(bind=engine)

# TDA Cola
class ColaMisiones:
    def __init__(self):
        self.items = []

    def enqueue(self, mision):
        self.items.append(mision)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def first(self):
        return self.items[0] if not self.is_empty() else None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

# FastAPI
app = FastAPI()
cola_personajes = {}

@app.post("/personajes")
def crear_personaje(nombre: str):
    db = SessionLocal()
    nuevo = Personaje(nombre=nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    cola_personajes[nuevo.id] = ColaMisiones()
    return nuevo

@app.post("/misiones")
def crear_mision(descripcion: str, xp: int):
    db = SessionLocal()
    nueva = Mision(descripcion=descripcion, xp_recompensa=xp)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.post("/personajes/{id}/misiones/{id_mision}")
def aceptar_mision(id: int, id_mision: int):
    db = SessionLocal()
    mision = db.query(Mision).get(id_mision)
    if mision:
        cola_personajes[id].enqueue(mision)
        return {"mensaje": "Misión aceptada"}
    raise HTTPException(status_code=404, detail="Misión no encontrada")

@app.post("/personajes/{id}/completar")
def completar_mision(id: int):
    db = SessionLocal()
    personaje = db.query(Personaje).get(id)
    if personaje and not cola_personajes[id].is_empty():
        mision = cola_personajes[id].dequeue()
        personaje.xp += mision.xp_recompensa
        db.commit()
        return {"mensaje": f"Misión completada: {mision.descripcion}"}
    raise HTTPException(status_code=404, detail="No hay misiones")

@app.get("/personajes/{id}/misiones")
def listar_misiones(id: int):
    if id in cola_personajes:
        cola = cola_personajes[id]
        return [m.descripcion for m in cola.items]
    raise HTTPException(status_code=404, detail="Personaje no encontrado")
