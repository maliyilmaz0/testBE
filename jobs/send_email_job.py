from .base import Job


class SendEmailJob(Job):
    def __init__(self, *args, **kwargs) -> None:
        self.mail_service = kwargs.get("mail_service", None)
        self.to = kwargs.get("to", "")
        self.subject = kwargs.get("subject", "")
        self.message = kwargs.get("message", "")
        super().__init__(*args, **kwargs)

    async def run(self, *args, **kwargs):
        try:
            await self.mail_service.send(self.to, self.subject, self.message)
        except Exception as e:
            raise Exception(f"JOB ERROR | {e}")
