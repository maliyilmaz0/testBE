import uuid


class StringHelper:

    @staticmethod
    def is_valid_uuid(id):
        try:
            uuid_obj = uuid.UUID(id)
            return True
        except:
            return False