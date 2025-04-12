# Usar una imagen base de Python
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1:
# Esta línea establece la variable de entorno PYTHONDONTWRITEBYTECODE a 1.
# Esto le indica a Python que no genere archivos .pyc (bytecode) cuando se ejecuten los scripts.
# Esto puede ser útil en entornos de desarrollo y despliegue para evitar la creación de archivos innecesarios y mantener el contenedor más limpio.
ENV PYTHONUNBUFFERED=1:
# Esta línea establece la variable de entorno PYTHONUNBUFFERED a 1.
# Esto le indica a Python que no haga buffering de la salida estándar (stdout) y la salida de error estándar (stderr).
# Esto es útil para que los logs se muestren en tiempo real, lo cual es importante para monitorear aplicaciones en contenedores.
# Instalar dependencias del sistema necesarias para compilar mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
# Establecer el directorio de trabajo
WORKDIR /code
# Copiar el archivo de requisitos y luego instalar dependencias
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
# Copiar todo el código del backend al contenedor
COPY . /code/
# Exponer el puerto 8000
# EXPOSE 8000
# Comando por defecto para correr el servidor de desarrollo de Django
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]