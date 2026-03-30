#!/usr/bin/env python3
"""
send_session_notification.py

Detects when a new session has been added to sesiones.org (first subsection
under the current year) and sends an HTML email notification via Resend.

Required environment variables (GitHub Secrets):
  RESEND_API_KEY     – API key for Resend
  EMAIL_RECIPIENTS   – Comma-separated list of recipient email addresses
  EMAIL_FROM         – Sender email address (default: onboarding@resend.dev for testing)
"""

import os
import re
import subprocess
import sys
from datetime import datetime

SESIONES_PATH = "content/TheComputationalGarage/sesiones.org"
WEB_URL = "https://statespaceeconometrics-mlearning-rgroup.github.io/TheComputationalGarage/sesiones.html"
DEFAULT_FROM_EMAIL = "onboarding@resend.dev"

SPANISH_WEEKDAYS = {
    0: "lunes",
    1: "martes",
    2: "miércoles",
    3: "jueves",
    4: "viernes",
    5: "sábado",
    6: "domingo",
}

SPANISH_MONTHS = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def _get_first_subsection_lines(org_lines):
    """Return the lines that belong to the first level-2 heading (** ...)."""
    inside = False
    section_lines = []
    for line in org_lines:
        if re.match(r"^\*{2} ", line):
            if inside:
                break  # end of first subsection
            inside = True
            section_lines.append(line)
        elif inside:
            section_lines.append(line)
    return section_lines


def parse_first_session(org_text):
    """
    Parse the first subsection (level-2 heading) from org_text.

    Returns a dict with keys: date, speakers, time, location.
    Returns None if the subsection cannot be found.
    """
    lines = org_text.splitlines()
    section = _get_first_subsection_lines(lines)
    if not section:
        return None

    data = {}

    # Date from heading title: ** YYYY-MM-DD
    title_match = re.match(r"^\*{2}\s+(\d{4}-\d{2}-\d{2})", section[0])
    if not title_match:
        return None
    data["date"] = title_match.group(1)

    # Properties block
    in_props = False
    for line in section[1:]:
        stripped = line.strip()
        if stripped == ":PROPERTIES:":
            in_props = True
            continue
        if stripped == ":END:":
            in_props = False
            continue
        if in_props:
            m = re.match(r":SPEAKERS:\s+(.+)", stripped)
            if m:
                data["speakers"] = m.group(1).strip()
            m = re.match(r":LOCATION:\s+(.+)", stripped)
            if m:
                data["location"] = m.group(1).strip()

    # Time from content: *Hora:* HH:MM
    for line in section:
        m = re.search(r"\*Hora:\*\s+(\d{1,2}:\d{2})", line)
        if m:
            data["time"] = m.group(1)
            break

    return data if "date" in data else None


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def get_previous_file_content():
    """Return the content of sesiones.org from the previous commit, or None."""
    try:
        result = subprocess.run(
            ["git", "show", f"HEAD^:{SESIONES_PATH}"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout
        # HEAD^ does not exist (first commit) or file didn't exist before
        return None
    except Exception as exc:
        print(f"[WARNING] Could not retrieve previous commit content: {exc}")
        return None


# ---------------------------------------------------------------------------
# Email building
# ---------------------------------------------------------------------------

def _format_date_spanish(date_str):
    """Convert 'YYYY-MM-DD' to 'lunes, 24 de marzo de 2026'."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        weekday = SPANISH_WEEKDAYS[dt.weekday()]
        month = SPANISH_MONTHS[dt.month]
        return f"{weekday}, {dt.day} de {month} de {dt.year}"
    except ValueError:
        return date_str


def build_html_email(session):
    date_str = session.get("date", "")
    date_formatted = _format_date_spanish(date_str)
    time_str = session.get("time", "–")
    speakers = session.get("speakers", "–")
    location = session.get("location", "–")

    # Subject date as DD/MM/YYYY
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        subject_date = dt.strftime("%d/%m/%Y")
    except ValueError:
        subject_date = date_str

    subject = f"Nueva sesión de The Computational Garage - {subject_date}"

    html_body = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"></head>
<body style="font-family: Arial, sans-serif; color: #222; max-width: 600px; margin: 0 auto; padding: 20px;">
  <p>Estimados/as compañeros/as,</p>
  <p>Os invitamos cordialmente a asistir a la próxima sesión de <strong>The Computational Garage</strong>:</p>
  <table style="border-collapse: collapse; margin: 16px 0;">
    <tr><td style="padding: 6px 12px;">📅 <strong>Fecha:</strong></td><td style="padding: 6px 12px;">{date_formatted}</td></tr>
    <tr><td style="padding: 6px 12px;">🕐 <strong>Hora:</strong></td><td style="padding: 6px 12px;">{time_str}</td></tr>
    <tr><td style="padding: 6px 12px;">👤 <strong>Ponente(s):</strong></td><td style="padding: 6px 12px;">{speakers}</td></tr>
    <tr><td style="padding: 6px 12px;">📍 <strong>Lugar:</strong></td><td style="padding: 6px 12px;">{location}</td></tr>
  </table>
  <p>Podéis consultar el histórico completo de sesiones en:<br>
     <a href="{WEB_URL}">{WEB_URL}</a>
  </p>
  <p>¡Os esperamos!</p>
  <hr style="border: none; border-top: 1px solid #ccc; margin: 24px 0;">
  <p style="font-size: 0.9em; color: #555;">
    The Computational Garage<br>
    State Space Econometrics &amp; Machine Learning Research Group<br>
    Universidad Complutense de Madrid
  </p>
</body>
</html>"""

    return subject, html_body


def build_plain_text_email(session):
    date_str = session.get("date", "")
    date_formatted = _format_date_spanish(date_str)
    time_str = session.get("time", "–")
    speakers = session.get("speakers", "–")
    location = session.get("location", "–")

    text = f"""Estimados/as compañeros/as,

Os invitamos cordialmente a asistir a la próxima sesión de The Computational Garage:

📅 Fecha: {date_formatted}
🕐 Hora: {time_str}
👤 Ponente(s): {speakers}
📍 Lugar: {location}

Podéis consultar el histórico completo de sesiones en:
{WEB_URL}

¡Os esperamos!

--
The Computational Garage
State Space Econometrics & Machine Learning Research Group
Universidad Complutense de Madrid
"""
    return text


# ---------------------------------------------------------------------------
# Resend sending
# ---------------------------------------------------------------------------

def send_email(subject, html_body, plain_text, recipients, from_email, api_key):
    """Send the notification email via Resend."""
    import resend

    resend.api_key = api_key

    # Resend expects a list of recipient emails
    to_list = [addr.strip() for addr in recipients if addr.strip()]
    if not to_list:
        print("[ERROR] No valid recipient addresses found.")
        return False

    try:
        params = {
            "from": from_email,
            "to": to_list,
            "subject": subject,
            "html": html_body,
            "text": plain_text,
        }

        response = resend.Emails.send(params)
        print(f"[INFO] Email sent successfully. ID: {response.get('id', 'N/A')}")
        return True
    except Exception as exc:
        print(f"[ERROR] Resend error: {exc}")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # --- Validate secrets ---
    api_key = os.environ.get("RESEND_API_KEY")
    recipients_raw = os.environ.get("EMAIL_RECIPIENTS")
    from_email = os.environ.get("EMAIL_FROM") or DEFAULT_FROM_EMAIL

    missing = [name for name, val in [
        ("RESEND_API_KEY", api_key),
        ("EMAIL_RECIPIENTS", recipients_raw),
    ] if not val]

    if missing:
        print(f"[ERROR] Missing required environment variables: {', '.join(missing)}")
        print("[INFO] Skipping notification. Please configure the GitHub Secrets.")
        sys.exit(0)  # exit 0 so the workflow does not fail

    recipients = [r.strip() for r in recipients_raw.split(",") if r.strip()]

    # --- Read current file ---
    try:
        with open(SESIONES_PATH, encoding="utf-8") as f:
            current_content = f.read()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {SESIONES_PATH}")
        sys.exit(0)

    current_session = parse_first_session(current_content)
    if not current_session:
        print("[INFO] No parseable session found in sesiones.org. Skipping notification.")
        sys.exit(0)

    print(f"[INFO] Current first session date: {current_session.get('date')}")

    # --- Check previous commit ---
    prev_content = get_previous_file_content()
    if prev_content is None:
        print("[INFO] No previous commit found (first run). Skipping notification.")
        sys.exit(0)

    prev_session = parse_first_session(prev_content)
    prev_date = prev_session.get("date") if prev_session else None
    print(f"[INFO] Previous first session date: {prev_date}")

    if current_session.get("date") == prev_date:
        print("[INFO] First session date unchanged. No notification needed.")
        sys.exit(0)

    print("[INFO] New session detected! Preparing notification email...")

    # --- Build and send email ---
    subject, html_body = build_html_email(current_session)
    plain_text = build_plain_text_email(current_session)

    print(f"[INFO] Subject: {subject}")
    print(f"[INFO] Sending to {len(recipients)} recipient(s)...")

    success = send_email(subject, html_body, plain_text, recipients, from_email, api_key)
    if not success:
        print("[WARNING] Email could not be sent. Continuing workflow without failing.")
    else:
        print("[INFO] Notification sent successfully.")


if __name__ == "__main__":
    main()
