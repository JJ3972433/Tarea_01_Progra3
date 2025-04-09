# Tarea_01_Progra3
Sistema de Misiones RPG con FastAPI en Programación 3

Este proyecto simula un sistema de misiones para personajes de un RPG usando FastAPI y SQLite.

 🔧 Tecnologías usadas en el desarrollo y ejecución:

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite

 🚀 Instalación:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/tu-repo.git
   cd tu-repo

Instala dependencias:
pip install fastapi uvicorn sqlalchemy

Ejecuta el servidor:
uvicorn main:app --reload

Abre la documentación interactiva:
http://127.0.0.1:8000/docs

📌 Endpoints principales:

POST /personajes – Crear un personaje

POST /misiones – Crear una misión

POST /personajes/{id}/misiones/{id_mision} – Aceptar misión

POST /personajes/{id}/completar – Completar misión

GET /personajes/{id}/misiones – Ver misiones en cola




