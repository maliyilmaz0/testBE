from services.db_service import DBService


class RepositoryService:
    repositories: {}

    def __init__(self, user_service: DBService,
                 user_details: DBService,
                 horoscopes: DBService,
                 roles: DBService,):
        self.repositories = {'user': user_service, 'user-detail': user_details, 'role': roles, 'horoscope': horoscopes}
