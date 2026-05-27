# Usa una imagen oficial de Python ligera
FROM python:3.12-slim

# Evita que Python escriba archivos .pyc y asegura que la salida en consola sea instantánea
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias para PostgreSQL y herramientas de compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requerimientos e instala las librerías de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Aseguramos la instalación de Gunicorn para el servidor de producción
RUN pip install --no-cache-dir gunicorn

# Copia todo el contenido del proyecto a la carpeta de trabajo del contenedor
COPY . /app/

# Expone el puerto 8000 que es donde escuchará Gunicorn
EXPOSE 8000

# Comando de producción ejecutando WSGI con Gunicorn
CMD ["gunicorn", "turismo_backend.wsgi:application", "--bind", "0.0.0.0:8000", "--access-logfile", "-"]