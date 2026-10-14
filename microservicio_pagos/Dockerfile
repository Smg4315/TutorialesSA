FROM python:3.11-alpine

# Directorio de trabajo dentro del contenedor.
WORKDIR /app

# Instala Flask y Gunicorn sin conservar la caché de pip.
RUN pip install --no-cache-dir Flask gunicorn

# Copia el código del microservicio al contenedor.
COPY . .

# Puerto en el que Gunicorn atenderá las solicitudes.
EXPOSE 5000

# Inicia la aplicación Flask mediante Gunicorn.
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]