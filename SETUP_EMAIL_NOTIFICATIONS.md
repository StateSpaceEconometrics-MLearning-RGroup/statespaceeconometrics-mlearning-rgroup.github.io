# Configuración del sistema de notificaciones por email

Este documento explica paso a paso cómo configurar el sistema de notificaciones automáticas por email para las sesiones de **The Computational Garage**.

Cada vez que se añada una nueva sesión en `content/TheComputationalGarage/sesiones.org` y se haga *push* a la rama `main`, GitHub Actions detectará el cambio y enviará automáticamente un email a la lista de destinatarios configurada.

---

## Requisitos previos

- Acceso de administrador al repositorio de GitHub.
- Una cuenta en [SendGrid](https://sendgrid.com) (gratuita hasta 100 emails/día).

---

## 1. Configurar SendGrid

### 1.1 Crear una cuenta gratuita

1. Ve a <https://sendgrid.com> y haz clic en **Start For Free**.
2. Rellena el formulario de registro con nombre, email y contraseña.
3. Confirma tu cuenta a través del email de verificación que recibirás.

### 1.2 Verificar el email remitente

SendGrid requiere que el email desde el que envías esté verificado.

1. En el panel de SendGrid, ve a **Settings → Sender Authentication**.
2. Elige **Single Sender Verification** (la opción más sencilla).
3. Rellena los datos del remitente:
   - **From Name**: `The Computational Garage`
   - **From Email**: el email que usaréis como remitente. Debe ser una dirección **real que controléis** y que podáis verificar (por ejemplo, `garage.ucm@gmail.com` o una cuenta de correo del departamento). Las direcciones de tipo `noreply@users.noreply.github.com` **no son verificables** en SendGrid.
   - **Reply To**: podéis dejarlo vacío o poner una dirección a la que sí queráis recibir respuestas.
4. Haz clic en **Create** y confirma la verificación desde el email que recibirás.

> **Nota:** Si prefieres usar un dominio propio, puedes hacer la verificación de dominio completa en **Domain Authentication**, pero no es necesario para empezar.

### 1.3 Crear una API Key

1. En el panel de SendGrid, ve a **Settings → API Keys**.
2. Haz clic en **Create API Key**.
3. Dale un nombre descriptivo, por ejemplo: `computational-garage-notifications`.
4. Selecciona **Restricted Access** y activa únicamente **Mail Send → Full Access**.
5. Haz clic en **Create & View**.
6. **Copia la API Key** que aparece en pantalla — solo se muestra una vez.

---

## 2. Configurar los GitHub Secrets

Los datos sensibles (API key y lista de emails) se almacenan como *Secrets* en GitHub, de modo que nunca quedan expuestos en el código fuente.

### 2.1 Acceder a la configuración de Secrets

1. Ve al repositorio en GitHub.
2. Haz clic en **Settings** (pestaña superior derecha).
3. En el menú lateral izquierdo, ve a **Secrets and variables → Actions**.
4. Haz clic en el botón **New repository secret**.

### 2.2 Crear los tres secrets necesarios

Repite el proceso de creación para cada uno de los siguientes secrets:

#### `SENDGRID_API_KEY`

- **Name**: `SENDGRID_API_KEY`
- **Secret**: pega aquí la API Key que copiaste de SendGrid.

#### `EMAIL_RECIPIENTS`

- **Name**: `EMAIL_RECIPIENTS`
- **Secret**: lista de direcciones de email separadas por comas.  
  Ejemplo: `persona1@ucm.es,persona2@ucm.es,persona3@ucm.es`  
  (los espacios alrededor de las comas son opcionales; el script los ignora automáticamente)

#### `EMAIL_FROM`

- **Name**: `EMAIL_FROM`
- **Secret**: la dirección de email verificada en SendGrid que usaréis como remitente.  
  Ejemplo: `garage.ucm@gmail.com`  
  (debe coincidir exactamente con el email verificado en el paso 1.2)

---

## 3. Probar el sistema

Una vez configurados los secrets, puedes verificar que todo funciona correctamente:

1. **Abre** el archivo `content/TheComputationalGarage/sesiones.org`.
2. **Añade una nueva subsección** con la próxima sesión, siguiendo el formato existente:
   ```
   ** YYYY-MM-DD
      :PROPERTIES:
      :HTML_CONTAINER_CLASS: session
      :SCHEDULED: <YYYY-MM-DD Day HH:MM>
      :SPEAKERS: Nombre del ponente
      :LOCATION: Aula XXX, Edificio YYY
      :END:

      - *Ponentes:* Nombre del ponente
      - *Hora:* HH:MM
      - *Lugar:* Aula XXX, Edificio YYY
   ```
   Recuerda colocarla **al principio** de la sección del año correspondiente, ya que el sistema siempre lee la primera subsección.

3. **Haz commit y push** a la rama `main`:
   ```bash
   git add content/TheComputationalGarage/sesiones.org
   git commit -m "Nueva sesión: YYYY-MM-DD"
   git push origin main
   ```

4. **Verifica el workflow** en GitHub:
   - Ve a la pestaña **Actions** del repositorio.
   - Busca la ejecución más reciente de **Push Web Deploy**.
   - Comprueba que el step *Enviar notificación de nueva sesión* aparece en verde.

5. **Confirma la recepción** del email en las cuentas de los destinatarios.

---

## 4. Resolución de problemas

| Síntoma | Posible causa | Solución |
|---------|---------------|----------|
| El step de notificación no aparece | `sesiones.org` no cambió en el commit | Comprueba que el archivo tiene cambios reales |
| Error `Missing required environment variables` | Secrets no configurados | Revisa el paso 2 de esta guía |
| Error de SendGrid 401 | API Key incorrecta | Regenera la API Key en SendGrid |
| Error de SendGrid 403 | Email remitente no verificado | Verifica el email en SendGrid (paso 1.2) |
| Email no llega | Dirección del destinatario incorrecta | Revisa el valor de `EMAIL_RECIPIENTS` |

---

## 5. Notas de seguridad

- Los emails de los destinatarios **nunca** deben aparecer en el código fuente.
- La API Key de SendGrid **nunca** debe subirse al repositorio.
- Si sospechas que alguna credencial ha quedado expuesta, revócala inmediatamente y crea una nueva.
- El script está diseñado para **no interrumpir el workflow** si hay un error en el envío del email: solo mostrará un aviso en el log.
