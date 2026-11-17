from App.Actor import Actor

class Administrator(Actor):
    dashboard_data = {}
    
    def __init__(self, admin_data_access_object):
        self.storage_key = "admin"
        self.data_gateway = admin_data_access_object
        self.base_route = "/admin/"