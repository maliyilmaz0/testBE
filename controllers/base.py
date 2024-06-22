from abc import ABC
from services.repo_service import RepositoryService
from services.logger_service import LoggerService


class BaseController(ABC):
    _logger: LoggerService
    _repositoryService: RepositoryService

    def __init__(self, logger, repositoryService):
        self._logger = logger
        self._repositoryService = repositoryService
