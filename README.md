# PrecioDeLibrosPY <img src="backend\static\books.256x256.png" height="30">

## Frontend 🎨

## Backend 🐍
### Instrucciones para Levantar el Backend con FastAPI

<details>
  <summary>Cómo levantar el Backend</summary>

  ### 📃 Requisitos previos
  Asegúrate de tener Python y el paquete `venv` instalados antes de seguir estos pasos.

  - Descarga e instala Python desde [python.org](https://www.python.org/downloads/)
  - Asegúrate de tener el paquete `venv` instalado (por lo general, está incluido con las versiones más recientes de Python)
  - abre la carpeta **Backend** desde tu terminal

  ### Crear un entorno virtual

  ```bash
  python -m venv venv
  ```

  Activar el entorno virtual:

  - En Windows:

    ```bash
    venv\Scripts\activate
    ```

  - En Linux/macOS:

    ```bash
    source venv/bin/activate
    ```

  Instalar los requisitos:
  ```bash
  pip install -r requirements.txt
  ```

  Prender la API con FastAPI:

  ```bash
  uvicorn main:app --reload
  ```

</details>

### Instructions to Set Up the Backend with FastAPI

<details>
  <summary>How to Set Up the Backend</summary>

  ### 📃 Prerequisites
  Make sure you have Python and the `venv` package installed before proceeding with these steps.

  - Download and install Python from [python.org](https://www.python.org/downloads/)
  - Ensure that the `venv` package is installed (it is usually included with the latest versions of Python)
  - open **backend** folder with your terminal

  ### Create a virtual environment

  ```bash
  python -m venv venv
  ```

  Activate the virtual environment:

  - On Windows:

    ```bash
    venv\Scripts\activate
    ```

  - On Linux/macOS:

    ```bash
    source venv/bin/activate
    ```

  Install the requirements:
  ```bash
  pip install -r requirements.txt
  ```

  Start the API with FastAPI:

  ```bash
  uvicorn main:app --reload
  ```

</details>