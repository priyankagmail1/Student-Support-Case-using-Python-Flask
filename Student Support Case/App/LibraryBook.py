class LibraryBook():
    item_id = 0
    title = ""
    version = ""
    publication_year = ""
    total_copies = 0
    is_available = False

    associated_course = {}

    def __init__(self, book_database_gateway):
        self.db_gateway = book_database_gateway