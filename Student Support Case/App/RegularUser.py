from App.Actor import Actor

class RegularUser(Actor):
    account_id = 0
    full_name = ""
    is_locked = False

    profile_data = {}

    def __init__(self, user_data_access_object):
        self.db_gateway = user_data_access_object
        self.storage_key = "user" # session storage key