# Usar una imagen base de Python
FROM python:3.11-slim


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
EXPOSE 8000

# Comando por defecto para correr el servidor de desarrollo de Django
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

