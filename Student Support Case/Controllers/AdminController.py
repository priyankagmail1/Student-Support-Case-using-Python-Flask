from App.Admin import Admin

class AdminController():
    def __init__(self, database_gateway):
        self.admin_account = Admin(database_gateway.db.admin)
        self.user_repository = database_gateway.db.user
        self.admin_repository = self.admin_account.dao

    def authenticate_admin(self, email_address, raw_password):
        admin_record = self.admin_repository.getByEmail(email_address)

        if admin_record is None:
            return False

        stored_password = admin_record["password"] # stored admin password
        if stored_password != raw_password:
            return False

        return admin_record
        
    def fetch_admin_by_id(self, admin_id):
        admin_record = self.admin_repository.getById(admin_id)

        return admin_record
        
    def retrieve_all_users(self):
        registered_users = self.user_repository.list()
        print(registered_users)

        return registered_users

    def logout_admin(self):
        self.admin_account.signout()

    def fetch_user_directory(self):
        return self.user_repository.list()