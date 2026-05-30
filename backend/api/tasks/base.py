from functools import lru_cache
from urllib.parse import urljoin

from django_cloud_tasks.tasks import Task, PublisherTask
from django_cloud_tasks.tasks.helpers import get_config


class SavageAimTask(Task):

    @classmethod
    @lru_cache()
    def url(cls) -> str:
        domain = get_config(name="domain")
        path = f'/tasks/tasks/{cls.name()}'
        return urljoin(domain, path)


class SavageAimPublisherTask(PublisherTask):

    @classmethod
    @lru_cache()
    def url(cls) -> str:
        domain = get_config(name="domain")
        path = f'/tasks/tasks/{cls.name()}'
        return urljoin(domain, path)
