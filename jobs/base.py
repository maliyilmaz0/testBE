from celery import Celery
from celery.result import AsyncResult
from config.global_config import global_config

celery = Celery(
    broker=global_config['redis_cli'],
    backend=global_config['redis_cli'],
)


class Job:
    def __init__(self, *args, **kwargs) -> None:
        pass

    async def run(self):
        raise NotImplementedError("Subclasses must implement the 'run' method.")


async def run_any_job(job_class: type(Job), *args, **kwargs):
    await job_class(*args, **kwargs).run()


@celery.task
async def celery_run_job(job_class: type(Job), *args, **kwargs):
    await run_any_job(job_class, *args, **kwargs)
