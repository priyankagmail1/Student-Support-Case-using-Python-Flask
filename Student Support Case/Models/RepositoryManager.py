from Models.DatabaseGateway import DatabaseGateway

class RepositoryManager():
    def __init__(self, application_context):
        self.database_adapter = DatabaseGateway(application_context)