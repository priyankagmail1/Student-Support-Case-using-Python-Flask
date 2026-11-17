from App.User import User


class MemberController():
    def __init__(self, database_gateway):
        self.member_entity = User(database_gateway.db.user)
        self.book_repository = database_gateway.db.book
        self.member_repository = self.member_entity.dao

    def fetch_all_members(self):
        all_members = self.member_repository.list()

        return all_members

    def authenticate_member(self, email_address, raw_password):
        member_record = self.member_repository.getByEmail(email_address)

        if member_record is None:
            return False

        stored_password = member_record['password'] # stored member password
        if stored_password != raw_password:
            return False

        return member_record

    def logout_member(self):
        self.member_entity.signout()
        
    def find_member_by_id(self, member_id):
        member_record = self.member_repository.getById(member_id)

        return member_record

    def register_member(self, full_name, email_address, raw_password):
        existing_member = self.member_repository.getByEmail(email_address)

        if existing_member is not None:
            return "already_exists"

        registration_payload = {"name": full_name, "email": email_address, "password": raw_password}
        
        created_member = self.member_repository.add(registration_payload)

        return created_member
        
    def retrieve_member_profile(self, member_id):
        member_record = self.member_repository.getById(member_id)

        return member_record
        
    def modify_member_details(self, full_name, email_address, raw_password, biography, member_id):
        updated_payload = {"name": full_name, "email": email_address, "password": raw_password, "bio": biography}
        
        updated_member = self.member_repository.update(updated_payload, member_id)

        return updated_member

    def fetch_member_borrowed_books(self, member_id):
        return self.book_repository.getBooksByUser(member_id)

    def fetch_book_borrowers(self, target_book_id):
        return self.member_repository.getUsersByBook(target_book_id)

