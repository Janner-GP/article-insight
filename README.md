# Proyecto Full Stack con Angular y FastAPI - Article Insight

Este proyecto es una aplicación web completa que incluye tanto el backend como el frontend. El backend está construido con FastAPI y el frontend está desarrollado con Angular.

## Contenido

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Despliegue](#despliegue)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Requisitos

Asegúrate de tener instalados los siguientes programas:

- Python (v3.8 o superior)
- Node.js (v14 o superior)
- npm (v6 o superior)
- Angular CLI (v12 o superior)

## Instalación

1. Clona el repositorio:

    ```sh
    git clone https://github.com/tu_usuario/tu_proyecto.git
    cd tu_proyecto
    ```

2. Instala las dependencias del backend:

    ```sh
    cd backend
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Instala las dependencias del frontend:

    ```sh
    cd ../frontend
    npm install
    ```

## Uso

### Backend

1. Inicia el servidor backend:

    ```sh
    cd backend
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    uvicorn app.main:app --reload
    ```

2. El servidor estará corriendo en `http://127.0.0.1:8000`.

### Frontend

1. Inicia la aplicación frontend:

    ```sh
    cd frontend
    ng serve
    ```

2. La aplicación estará disponible en `http://localhost:4200`.

## Despliegue

### Backend

Para desplegar el backend en un servidor, puedes usar un servidor ASGI como Uvicorn o Daphne junto con un servidor proxy como Nginx.

### Frontend

Para desplegar el frontend, puedes compilar la aplicación y servir los archivos estáticos desde un servidor web como Nginx o Apache:

```sh
cd frontend
ng build --prod
```