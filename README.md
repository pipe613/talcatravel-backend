# TalcaTravel Tech - Sistema de Reservas Turísticas

Plataforma de gestión y reserva de tours turísticos, desarrollada con una arquitectura basada en microservicios y despliegue continuo (CI/CD) en la nube. 

Este proyecto implementa una separación completa entre el cliente móvil y el servidor, asegurando alta disponibilidad, escalabilidad y automatización de procesos operativos.

## 🚀 Arquitectura y Tecnologías

El ecosistema del proyecto está compuesto por las siguientes tecnologías:

* **Frontend Móvil:** Flutter (Dart). Consumo de API RESTful, gestión de estado y UI reactiva.
* **Backend API:** Django REST Framework (Python). Lógica de negocio, serialización de datos y endpoints seguros.
* **Base de Datos:** PostgreSQL Serverless (Neon). Almacenamiento persistente desacoplado de la instancia de cómputo.
* **Infraestructura Cloud:** Amazon Web Services (AWS EC2). Instancia base para el alojamiento del entorno.
* **Orquestación de Contenedores:** Kubernetes ligero (K3s). Gestión de réplicas, balanceo de carga interno y Zero-Downtime Deployments.
* **Contenedorización:** Docker. Empaquetado eficiente utilizando imágenes optimizadas (`python:3.12-slim`).
* **CI/CD:** GitHub Actions. Pipeline automatizado para construcción de imágenes y actualización del clúster.

## ⚙️ Características Principales

1. **Catálogo Dinámico:** Consumo en tiempo real de los tours disponibles desde la base de datos PostgreSQL.
2. **Gestión de Reservas (CRUD):** Creación, lectura, actualización (pasajeros/fecha) y cancelación de reservas.
3. **Lógica de Negocios Centralizada:** El cálculo de precios totales es manejado tanto de forma visual en la app como a nivel de base de datos para garantizar consistencia.
4. **Despliegue Continuo (CI/CD):** Cada `push` a la rama `main` dispara un flujo de trabajo que empaqueta la nueva versión en Docker Hub y reinicia los pods en Kubernetes automáticamente sin interrumpir el servicio.

## 🛠️ Estructura de Infraestructura como Código (IaC)

El proyecto incluye manifiestos de Kubernetes en el directorio `k8s/`:
* `deployment.yaml`: Define las réplicas de los contenedores, la política de actualización (`Always`) y las variables de entorno inyectadas a través de Secrets.
* `service.yaml`: Configura el balanceador de carga que expone el puerto interno 8000 hacia el tráfico externo mediante la IP pública del servidor AWS.

## 📖 Instrucciones de Despliegue Local (Entorno de Desarrollo)

Para levantar el entorno backend en una máquina local:

1. Clonar el repositorio.
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno virtual:
   * Windows: `venv\Scripts\activate`
   * Linux/Mac: `source venv/bin/activate`
4. Instalar las dependencias: `pip install -r requirements.txt`
5. Configurar las variables de entorno (Base de datos Neon) en un archivo `.env`.
6. Aplicar las migraciones: `python manage.py migrate`
7. Ejecutar el servidor de desarrollo: `python manage.py runserver`

Para la aplicación móvil:
1. Navegar al directorio de Flutter.
2. Ejecutar `flutter pub get` para descargar dependencias.
3. Ejecutar `flutter run` con un dispositivo o emulador conectado.

## 🔄 Flujo CI/CD (GitHub Actions)

El archivo `.github/workflows/deploy.yml` define las siguientes fases operativas:
1. **Verify:** Comprueba la integridad del `Dockerfile` en un entorno aislado.
2. **Build & Push:** Autentica con Docker Hub, compila la imagen ignorando la caché anterior y la sube al registro de contenedores.
3. **Deploy:** Conexión segura vía SSH al clúster de AWS EC2 para ejecutar el comando `kubectl rollout restart deployment`, aplicando los cambios en vivo en los microservicios.