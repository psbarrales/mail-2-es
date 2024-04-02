import imaplib
import os
import logging
import re
import email
from bs4 import BeautifulSoup
from email.header import decode_header
from typing import List
from domain.entities.Mail import Mail
from domain.repositories.IMailingServicePort import IMailingServicePort


GOOGLE_IMAP_URL = "imap.gmail.com"


class GmailMailService(IMailingServicePort):
    mail: imaplib.IMAP4_SSL = None

    def connect(self):
        self.mail = imaplib.IMAP4_SSL(GOOGLE_IMAP_URL)
        logging.info("Email connecting...")
        self.mail.login(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PWD"))
        self.mail.select(os.getenv("MAIL_BOX"))
        logging.info("Email connected")

    def get_emails(self):
        mails: List[Mail] = []
        _, messages = self.mail.search(None, "UNSEEN")
        messages = messages[0].split()
        for mail_id in messages:
            subject, date, content = self._get_mail_content(mail_id, True)
            mails.append(Mail(id=mail_id, subject=subject, content=content, date=date))

        return mails

    def _get_mime_type(self, msg):
        content_type = msg.get_content_maintype()
        if content_type == "multipart":
            for part in msg.walk():
                if part.get_content_maintype() == "text":
                    return part.get_content_type()
        elif content_type == "text":
            return msg.get_content_type()
        return ""

    def _safe_decode(self, content, encoding="utf-8", errors="replace"):
        try:
            if isinstance(content, str):
                return content
            return content.decode(encoding, errors=errors)
        except UnicodeDecodeError:
            # Si la decodificación con UTF-8 falla, intenta con otra codificación común
            return content.decode("iso-8859-1", errors=errors)

    def _get_mail_content(self, mail_id: str, readonly: bool = True):
        status, data = self.mail.fetch(
            mail_id, "(BODY.PEEK[])" if readonly else "(RFC822)"
        )

        # status, data = mail.fetch(mail_id, "(BODY.PEEK[])")
        # logging.info(mail_id, status, data)
        # mail_content = BeautifulSoup(mail_html_content, "lxml")
        # logging.info(mail_content.get_text())
        # system_prompt, reduced_content = sc(mail_content.get_text())
        # logging.info(system_prompt)
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                # Decodificar el asunto
                subject, encoding = decode_header(message["Subject"])[0]
                subject = self._safe_decode(subject, encoding or "utf-8")
                date, _ = decode_header(message["Date"])[0]
                html_body = ""
                # Revisar si el mensaje es multipart
                if message.is_multipart():
                    for part in message.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        # Buscar la parte con contenido HTML
                        if (
                            content_type == "text/html"
                            and "attachment" not in content_disposition
                        ):
                            html_body = self._safe_decode(
                                part.get_payload(decode=True), encoding or "utf-8"
                            )
                            # Aquí puedes procesar el HTML como necesites
                            break  # Suponiendo que solo quieres el primer fragmento HTML
                else:
                    # Si el mensaje no es multipart, simplemente obtén el cuerpo
                    content_type = self._get_mime_type(message)
                    if content_type == "text/html" or content_type == "text/plain":
                        html_body = self._safe_decode(
                            message.get_payload(decode=True), encoding or "utf-8"
                        )
                        # Procesar el HTML como necesites

                mail_content = BeautifulSoup(html_body, "lxml")
                mail_text = mail_content.get_text()
                mail_clean_lines = re.sub(r"\n\s*\n", "\n", mail_text)
                mail_clean = re.sub(r"[ \t]+", " ", mail_clean_lines).strip()
                # mail_reduced, reduced_content = sc(mail_clean)
                content = mail_clean
        return subject, date, content

    def commit(self, id_mail):
        self.mail.fetch(id_mail, "(RFC822)")
        self.mail.store(id_mail, "+FLAGS", "\\Seen")

    def disconnect(self):
        self.mail.close()
        self.mail.logout()
        logging.info("Email disconnected")
        self.mail = imaplib.IMAP4_SSL(GOOGLE_IMAP_URL)
