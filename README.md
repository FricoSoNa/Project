# Proyecto Urban Routes

## Descripción del proyecto

Este proyecto consiste en realizar pruebas automatizadas en la aplicación Urban Routes, con el objetivo de comprobar que sus principales funciones trabajen correctamente.

Se realizaron pruebas para ingresar una ruta, seleccionar el tipo de taxi, agregar un número telefónico, registrar una tarjeta bancaria y configurar algunas opciones del viaje antes de solicitar un taxi.

## Tecnologías utilizadas

Para realizar este proyecto se utilizaron las siguientes herramientas:

- **Python:** lenguaje utilizado para escribir el código.
- **Selenium:** herramienta para automatizar las acciones dentro del navegador.
- **Pytest:** utilizado para ejecutar las pruebas y comprobar los resultados.
- **Google Chrome:** navegador utilizado para realizar las pruebas.
- **PyCharm:** programa utilizado para escribir y ejecutar el código.

También se utilizaron localizadores como ID, XPath y CSS Selector para encontrar los elementos de la página, así como esperas para permitir que los elementos cargaran correctamente.

## Cómo ejecutar las pruebas

1. Tener instalado Python y Google Chrome.
2. Abrir el proyecto en PyCharm.
3. Abrir la terminal e instalar las herramientas necesarias con el siguiente comando:

```bash
pip install selenium pytest
```

4. Para ejecutar las pruebas, escribir en la terminal:

```bash
pytest
```

5. Al terminar, Pytest mostrará los resultados e indicará si las pruebas fueron exitosas o si ocurrió algún error.

## Archivos del proyecto

- `main.py`: contiene el código y las pruebas automatizadas.
- `data.py`: contiene los datos utilizados para realizar las pruebas.