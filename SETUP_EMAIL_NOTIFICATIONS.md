# Configuración de Notificaciones por Email

Este documento describe cómo configurar las notificaciones automáticas por email usando **Gmail SMTP**.

## ¿Por qué Gmail?

Gmail SMTP es una solución confiable y gratuita que permite:
- ✅ Enviar hasta 500 emails por día
- ✅ Enviar a múltiples destinatarios sin verificación de dominio
- ✅ Usar autenticación segura con contraseñas de aplicación
- ✅ No requiere configuración DNS

---

## Cuenta ya configurada

La cuenta **thecomputationalgarage@gmail.com** ya está configurada y lista para usar. Los mantenedores del repositorio tienen acceso a las credenciales.

---

## GitHub Secrets Configurados

Los siguientes secrets ya están configurados en GitHub Actions:

| Secret | Descripción | Valor |
|--------|-------------|-------|
| `EMAIL_USER` | Dirección de Gmail | `thecomputationalgarage@gmail.com` |
| `EMAIL_PASSWORD` | Contraseña de aplicación de Gmail | (16 caracteres - configurada) |
| `EMAIL_RECIPIENTS` | Lista de destinatarios | Emails separados por comas |

---

## Modificar la lista de destinatarios

Para cambiar quién recibe las notificaciones:

1. Ve a **Settings** del repositorio
2. **Secrets and variables** → **Actions**
3. Haz clic en **EMAIL_RECIPIENTS** → **Update secret**
4. Modifica la lista de emails (formato: `email1@ucm.es,email2@ucm.es,email3@ucm.es`)
5. **IMPORTANTE:** Sin espacios después de las comas
6. Haz clic en **Update secret**

---

## Cómo funciona

Cada vez que se actualiza el archivo `content/TheComputationalGarage/sesiones.org` y la fecha de la primera sesión cambia:

1. GitHub Actions detecta el cambio automáticamente
2. El script extrae los detalles de la sesión (fecha, ponentes, hora, lugar)
3. Se envía un email HTML desde `thecomputationalgarage@gmail.com`
4. Todos los emails en `EMAIL_RECIPIENTS` reciben la invitación

---

## Solución de problemas

### El email no se envió

**Verifica:**
1. Ve a **Actions** → última ejecución del workflow
2. Expande el step "Enviar notificación de nueva sesión"
3. Busca mensajes de error en los logs

**Errores comunes:**
- `[ERROR] SMTP error: (535, ...)` → Contraseña de aplicación incorrecta
- `[ERROR] No valid recipient addresses found` → Lista de emails vacía o mal formateada
- `[INFO] First session date unchanged` → La fecha de la sesión no cambió

### Regenerar contraseña de aplicación

Si es necesario crear una nueva contraseña de aplicación:

1. Inicia sesión en Gmail con `thecomputationalgarage@gmail.com`
2. Ve a **Cuenta de Google** → **Seguridad**
3. **Verificación en dos pasos** → **Contraseñas de aplicaciones**
4. Genera una nueva contraseña (16 caracteres)
5. Actualiza el secret `EMAIL_PASSWORD` en GitHub
6. Revoca la contraseña anterior

---

## Límites de Gmail

- **500 emails por día** (más que suficiente para este uso)
- **100 destinatarios por email**
- Retraso de ~1 segundo entre envíos

---

## Información de contacto

Para problemas con la cuenta de Gmail o las notificaciones, contacta a los mantenedores del repositorio.

