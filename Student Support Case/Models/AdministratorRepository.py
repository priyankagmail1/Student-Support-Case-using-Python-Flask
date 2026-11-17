class AdministratorRepository():
    connection = {}
    
    def __init__(self, database_adapter):
        self.connection = database_adapter
        self.connection.table = "admin"

    def fetch_by_identifier(self, admin_id):
        cursor_result = self.connection.query("select * from @table where id='{}'".format(admin_id))

        admin_record = cursor_result.fetchone()

        return admin_record

    def fetch_by_email_address(self, email_address):
        cursor_result = self.connection.query("select * from @table where email='{}'".format(email_address))

        admin_record = cursor_result.fetchone()

        return admin_record