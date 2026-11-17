from App.Books import Books

class LibraryCatalogController():
    def __init__(self, database_gateway):
        self.book_entity = Books(database_gateway.db.book)
        self.book_repository = self.book_entity.dao

    def fetch_catalog(self, is_available=1, member_id=None):
        if member_id != None:
            catalog_items = self.book_repository.listByUser(member_id)
        else:
            catalog_items = self.book_repository.list(is_available)

        return catalog_items

    def retrieve_member_reservations(self, member_id):
        reserved_items = self.book_repository.getReserverdBooksByUser(member_id)

        return reserved_items

    def find_book_by_id(self, book_identifier):
        book_record = self.book_repository.getBook(book_identifier)

        return book_record

    def query_books(self, search_term, is_available=1):
        matching_books = self.book_repository.search_book(search_term, is_available)

        return matching_books

    def place_reservation(self, member_id, target_book_id):
        reservation_result = self.book_repository.reserve(member_id, target_book_id)

        return reservation_result

    def retrieve_member_books(self, member_id):
        borrowed_books = self.book_repository.getBooksByUser(member_id)

        return borrowed_books

    def count_member_books(self, member_id):
        total_borrowed = self.book_repository.getBooksCountByUser(member_id)

        return total_borrowed

    def remove_book(self, book_identifier):
        self.book_repository.delete(book_identifier)