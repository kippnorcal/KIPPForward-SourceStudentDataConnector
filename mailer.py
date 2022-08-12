import os

import requests


class Mailer:
    def __init__(self, job_name):
        self.job_name = job_name
        self.mg_api_key = os.getenv("MG_API_KEY")
        self.mg_domain = os.getenv("MG_DOMAIN")
        self.mg_api_url = os.getenv("MG_API_URL")
        self.from_address = os.getenv("SENDER_EMAIL")
        self.to_address = os.getenv("RECIPIENT_EMAIL")
        self.error_message = None

    def _subject_line(self):
        """Job status notification: Return formatted subject line based on error message content"""
        subject_type = "Error" if self.error_message else "Success"
        return f"{self.job_name} - {subject_type}"

    def _body_text(self):
        """Job status notification: Return formatted body text based on error message content."""
        if self.error_message:
            return f"{self.job_name} encountered an error.\n{self.error_message}"
        else:
            return f"{self.job_name} completed successfully."

    @staticmethod
    def _attachments():
        """Return list of attachments (in this case, logs)"""
        filename = "../app.log"
        if os.path.exists(filename):
            return [("attachment", (filename, open(filename, "rb").read()))]

    def notify(self, error_message=None):
        """Send email success/error notifications using Mailgun API."""
        self.error_message = error_message
        requests.post(
            f"{self.mg_api_url}{self.mg_domain}/messages",
            auth=("api", self.mg_api_key),
            files=self._attachments(),
            data={
                "from": self.from_address,
                "to": self.to_address,
                "subject": self._subject_line(),
                "text": self._body_text(),
            },
        )
