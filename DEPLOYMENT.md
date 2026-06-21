# Guía de Aprovisionamiento y Despliegue en GCP - Dominikito

Esta guía detalla el proceso paso a paso para aprovisionar la infraestructura en Google Cloud Platform (GCP) utilizando Terraform, y desplegar la aplicación backend (Cloud Run) y los agentes (Agent Registry / Vertex AI Reasoning Engines).

---

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado y configurado lo siguiente:

1. **Google Cloud SDK (`gcloud`)**: [Instrucciones de instalación](https://cloud.google.com/sdk/docs/install).
2. **Terraform**: [Instrucciones de instalación](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).
3. **Autenticación local en GCP**:
   Inicia sesión en tu cuenta de GCP y configura tus credenciales predeterminadas de aplicación (ADC):
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```
4. **Permisos en GCP**: Tu usuario debe tener rol de Administrador o Propietario en el proyecto GCP para poder habilitar APIs y crear cuentas de servicio e IAM bindings.

---

## 🌍 Configuración de Variables del Shell

Para facilitar la ejecución de los comandos a lo largo de esta guía, define los IDs de tus proyectos como variables en tu terminal:

```bash
export GCP_PROJECT_ID="TU_GCP_PROJECT_ID"
export FIREBASE_PROJECT_ID="TU_FIREBASE_PROJECT_ID"
```

---

## 🛠️ Fase 1: Aprovisionamiento de Infraestructura (Terraform)

En esta fase, Terraform habilitará automáticamente las APIs necesarias de GCP, creará un bucket para el almacenamiento de los agentes y creará las cuentas de servicio personalizadas con privilegios mínimos para mitigar riesgos.

1. Navega al directorio de Terraform:
   ```bash
   cd terraform
   ```

2. Verifica y ajusta el archivo `terraform.tfvars`. El contenido por defecto es:
   ```hcl
   project_id          = "TU_GCP_PROJECT_ID"
   firebase_project_id = "TU_FIREBASE_PROJECT_ID"
   region              = "us-central1"
   app_name            = "dominikito"
   ```

3. Inicializa Terraform para descargar los proveedores necesarios:
   ```bash
   terraform init
   ```

4. Genera y revisa el plan de ejecución:
   ```bash
   terraform plan
   ```

5. Aplica los cambios para crear los recursos en GCP:
   ```bash
   terraform apply
   ```
   *(Escribe `yes` cuando se te solicite confirmación)*.

Al finalizar con éxito, Terraform imprimirá los valores de salida (outputs) que necesitarás en el siguiente paso.

---

## 🔑 Fase 2: Configuración de Entorno (`.env`)

Usa los outputs generados por Terraform para rellenar tu archivo `.env` en el backend.

1. Ve a la carpeta del backend:
   ```bash
   cd ../backend
   ```
2. Si no lo has hecho, copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```
3. Configura las siguientes variables requeridas por el backend y el script de despliegue en `backend/.env`:

   ```env
   # Credenciales GCP obtenidas del despliegue de Terraform
   GCP_PROJECT_ID="TU_GCP_PROJECT_ID"
   GCP_REGION="us-central1"
   GCS_STAGING_BUCKET="dominikito-staging-TU_GCP_PROJECT_ID"
   GCP_SERVICE_ACCOUNT="dominikito-agent-sa@TU_GCP_PROJECT_ID.iam.gserviceaccount.com"

   # Claves y configuraciones de servicios externos
   GOOGLE_API_KEY="TU_GEMINI_API_KEY" # Opcional si se ejecuta local sin ADC
   ELEVENLABS_API_KEY="TU_ELEVENLABS_API_KEY"
   SUPABASE_URL="TU_SUPABASE_URL"
   SUPABASE_SERVICE_ROLE_KEY="TU_SUPABASE_SERVICE_ROLE_KEY"
   DASHBOARD_PIN="1234"
   ```

---

## 🤖 Fase 3: Despliegue de Agentes a Agent Registry (Vertex AI)

El script de despliegue empaquetará los módulos del backend y subirá los tres agentes (`cuentista`, `dilemas`, `narrador`) como Reasoning Engines en la plataforma Vertex AI de GCP.

1. Asegúrate de estar en el directorio `backend/` y tener activado tu entorno virtual `.venv`:
   ```bash
   source .venv/bin/activate
   ```
2. Ejecuta el script de despliegue:
   ```bash
   python deploy_agents.py
   ```
   El script utilizará los valores definidos en tu archivo `.env` para subir y registrar los agentes. Si el comando se ejecuta con éxito, imprimirá los **Resource Names** de cada Reasoning Engine en la consola.

---

## 🚀 Fase 4: Despliegue del Backend en Cloud Run

La aplicación FastAPI del backend se desplegará en un contenedor administrado por Cloud Run utilizando la cuenta de servicio personalizada `dominikito-run-sa`.

1. Compila la imagen de Docker utilizando Google Cloud Build y súbela a Container Registry:
   ```bash
   gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/dominikito-backend
   ```

2. Despliega la imagen en Cloud Run asociándola a su cuenta de servicio dedicada y pasando los secretos y variables de entorno del archivo `.env`:
   ```bash
   gcloud run deploy dominikito-backend \
     --image gcr.io/$GCP_PROJECT_ID/dominikito-backend \
     --service-account dominikito-run-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars="DASHBOARD_PIN=1234,GCP_PROJECT_ID=$GCP_PROJECT_ID,GCP_REGION=us-central1" \
     --set-secrets="ELEVENLABS_API_KEY=elevenlabs-api-key:latest,SUPABASE_URL=supabase-url:latest,SUPABASE_SERVICE_ROLE_KEY=supabase-service-role-key:latest"
   ```
   
   > 💡 **Tip sobre Secretos:** En producción, es altamente recomendable crear previamente los secretos en GCP Secret Manager utilizando `gcloud secrets create` y luego pasarlos al comando mediante `--set-secrets` como se describe arriba para no exponer claves en texto plano en la configuración del servicio.

Al terminar, Cloud Run te proporcionará la **Service URL** pública de la aplicación backend (ej. `https://dominikito-backend-xxxxxx.a.run.app`).

---

## 🌐 Conexión de Frontend (Firebase)

El frontend que reside en los archivos `backend/web` y se comunica con Firebase en el cliente (Auth, Firestore y Storage) ahora se conectará con los endpoints HTTPS de la aplicación que se encuentra en la **Service URL** del Cloud Run backend que acabas de desplegar.
