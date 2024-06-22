from abc import ABC, abstractmethod
from aiosmtplib import SMTP
from email.mime.text import MIMEText


class BaseMailService(ABC):
    _server: SMTP

    def __init__(self, host, port, username, password):
        self._server = SMTP(hostname=host, port=port)

    @abstractmethod
    async def send(self, to, subject, message):
        pass


# (API)
# (SMTP)
class SMTPMailService(BaseMailService):

    def __init__(self, host, port, username, password):
        super().__init__(host, port, username, password)
        self.__username = username
        self.__password = password
        self.__email = "m.ali.software.dev@gmail.com"
        

    async def send(self, to, subject, message):
        try:
            await self._server.connect()
            await self._server.ehlo()
            await self._server.login(self.__username, self.__password)
            sender_email = self.__email
            receiver = to
            subject = subject
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = receiver
            await self._server.sendmail(sender_email, receiver, msg.as_string())
        except Exception as e:
            raise e
        finally:
            await self._server.quit()


class APIMailService(BaseMailService):
    def __init__(self, host, port, username, password):
        super().__init__(host, port, username, password)

    async def send(self, to, subject, message):
        # mail gönderme işlemini API'ye göre yap.
        pass
