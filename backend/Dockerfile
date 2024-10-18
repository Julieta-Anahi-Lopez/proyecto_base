# Utiliza una imagen oficial de Python 3.11 slim como base
FROM python:3.11-slim



# Instalar las dependencias del sistema necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /code

# Copia los archivos de requisitos y luego instala dependencias
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código del backend al contenedor
COPY . /code/

# Exponer el puerto 8000
EXPOSE 8000

# Comando por defecto para correr el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
