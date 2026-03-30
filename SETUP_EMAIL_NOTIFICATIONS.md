# Configuración de Notificaciones por Email

Este documento describe cómo configurar las notificaciones automáticas por email usando **Resend**.

## ¿Por qué Resend?

Resend es mucho más simple de configurar que SendGrid para sitios en GitHub Pages:
- ✅ No requiere verificación DNS
- ✅ Puedes empezar inmediatamente con `onboarding@resend.dev`
- ✅ 100 emails gratis al día (3,000 al mes)
- ✅ API muy simple

---

## Paso 1: Crear cuenta en Resend

1. Ve a [https://resend.com/signup](https://resend.com/signup)
2. Regístrate con tu email (puedes usar Gmail, email institucional, etc.)
3. Verifica tu email
4. Inicia sesión en [https://resend.com](https://resend.com)

---

## Paso 2: Obtener API Key

1. En el dashboard de Resend, ve a **API Keys** (en el menú lateral)
2. Haz clic en **Create API Key**
3. Dale un nombre descriptivo (ej: `GitHub Actions - Computational Garage`)
4. Selecciona el permiso **Sending access**
5. Haz clic en **Add**
6. **Copia la API key** (empieza con `re_...`) - solo la verás una vez
7. Guárdala en un lugar seguro temporalmente

---

## Paso 3: Configurar GitHub Secrets

1. Ve al repositorio en GitHub
2. Haz clic en **Settings** (configuración del repositorio)
3. En el menú lateral, ve a **Secrets and variables** → **Actions**
4. Haz clic en **New repository secret**

### Secret 1: `RESEND_API_KEY`

- **Name:** `RESEND_API_KEY`
- **Value:** La API key que copiaste de Resend (ej: `re_xxxxxxxxxxxxx`)
- Haz clic en **Add secret**

### Secret 2: `EMAIL_RECIPIENTS`

- **Name:** `EMAIL_RECIPIENTS`
- **Value:** Lista de emails separados por comas (ej: `email1@ucm.es,email2@ucm.es,email3@ucm.es`)
- Haz clic en **Add secret**

### Secret 3: `EMAIL_FROM` (OPCIONAL)

- **Name:** `EMAIL_FROM`
- **Value:** `onboarding@resend.dev` (o tu dominio verificado si tienes uno)
- Haz clic en **Add secret**

> **Nota:** Si no configuras `EMAIL_FROM`, se usará automáticamente `onboarding@resend.dev`

---

## Paso 4: Probar el sistema

### Prueba manual:

1. Edita `content/TheComputationalGarage/sesiones.org`
2. Modifica la **fecha** de la primera subsección (la más reciente)
3. Haz commit y push:
   ```bash
   git add content/TheComputationalGarage/sesiones.org
   git commit -m "test: probar notificación de sesión"
   git push
   ```
4. Ve a **Actions** en GitHub y espera a que se ejecute el workflow
5. Revisa los logs del step "Enviar notificación de nueva sesión"
6. Verifica que los destinatarios recibieron el email

---

## Solución de problemas

### El email no llega

1. **Revisa la carpeta de spam** - los primeros emails pueden caer ahí
2. **Verifica los logs** en GitHub Actions para ver si hay errores
3. **Comprueba los secrets** - asegúrate de que `RESEND_API_KEY` y `EMAIL_RECIPIENTS` están configurados
4. **Revisa el dashboard de Resend** en [https://resend.com/emails](https://resend.com/emails) para ver el estado de los envíos

### Error "API key not found"

- Verifica que el secret `RESEND_API_KEY` está correctamente configurado
- La API key debe empezar con `re_`

### Error "Invalid from address"

- Si usas un dominio personalizado, debe estar verificado en Resend
- Para pruebas, usa `onboarding@resend.dev` (no requiere verificación)

### Los emails se marcan como spam

- Usa `onboarding@resend.dev` como remitente para empezar
- Si quieres emails más profesionales, considera comprar un dominio (~10€/año) y verificarlo en Resend

---

## Actualizar lista de destinatarios

Para cambiar quién recibe las notificaciones:

1. Ve a **Settings** → **Secrets and variables** → **Actions**
2. Haz clic en `EMAIL_RECIPIENTS`
3. Haz clic en **Update**
4. Modifica la lista de emails (separados por comas)
5. Haz clic en **Update secret**

---

## Límites del plan gratuito

Resend plan gratuito:
- 100 emails/día
- 3,000 emails/mes
- Sin necesidad de tarjeta de crédito

Para este proyecto (notificaciones de sesiones), es más que suficiente.

---

## Migrar a dominio personalizado (opcional)

Si en el futuro quieres emails desde tu propio dominio (ej: `noreply@tugrupo.com`):

1. Compra un dominio en Namecheap, Google Domains, etc. (~10€/año)
2. En Resend dashboard, ve a **Domains** → **Add Domain**
3. Sigue las instrucciones para agregar registros DNS
4. Una vez verificado, actualiza el secret `EMAIL_FROM` con tu nuevo dominio

---

## Recursos adicionales

- [Documentación de Resend](https://resend.com/docs)
- [Resend Python SDK](https://github.com/resend/resend-python)
- [Dashboard de Resend](https://resend.com)

