# Imagen base de Python ligera para ejecutar Django.
FROM python:3.11-slim

# Evita archivos .pyc y envía los logs directamente a la salida del contenedor.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor.
WORKDIR /app

# Instala las bibliotecas de sistema requeridas para dependencias de PostgreSQL.
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala las dependencias de Python antes de copiar el código de la aplicación.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del proyecto.
COPY . .

# Puerto interno de Gunicorn; Nginx publica la aplicación hacia el exterior.
EXPOSE 8000

# Inicia Django con Gunicorn, igual que el servicio web_django de Compose.
CMD ["gunicorn", "Tienda.wsgi:application", "--bind", "0.0.0.0:8000"]