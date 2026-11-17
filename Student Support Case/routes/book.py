from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response
from app import DAO

from Controllers.MemberController import MemberController
from Controllers.LibraryCatalogController import LibraryCatalogController

book_view = Blueprint('book_routes', __name__, template_folder='/templates')

library_catalog_controller = LibraryCatalogController(DAO)
member_controller = MemberController(DAO)

@book_view.route('/books/', defaults={'book_id': None})
@book_view.route('/books/<int:book_id>')
def home(book_id):
	member_controller.member_entity.configure_context(session, g)

	if book_id != None:
		target_book = library_catalog_controller.find_book_by_id(book_id)

		print('----------------------------')
		print(target_book)

		borrowed_book_ids = {}
		if member_controller.member_entity.is_authenticated():
			reservation_record = library_catalog_controller.retrieve_member_reservations(member_id=member_controller.member_entity.get_identifier())
			if reservation_record and 'user_books' in reservation_record:
				borrowed_book_ids = reservation_record['user_books'].split(',')
		
		if target_book and len(target_book) < 1:
			return render_template('book_view.html', error="No book found!")

		return render_template("book_view.html", books=target_book, g=g, user_books=borrowed_book_ids)
	else:
		catalog_items = library_catalog_controller.fetch_catalog()

		borrowed_book_ids = []
		if member_controller.member_entity.is_authenticated():
			active_reservations = library_catalog_controller.retrieve_member_reservations(member_id=member_controller.member_entity.get_identifier())
			
			if active_reservations is not None and 'user_books' in active_reservations:
				borrowed_book_ids = active_reservations['user_books'].split(',')
		
		print("---------------------------------------")
		print(borrowed_book_ids)

		if catalog_items and len(catalog_items) < 1:
			return render_template('books.html', error="No books found!")
	
		return render_template("books.html", books=catalog_items, g=g, user_books=borrowed_book_ids)

	return render_template("books.html", books=catalog_items, g=g)


@book_view.route('/books/add/<int:book_id>', methods=['GET'])
@member_controller.member_entity.auth_required
def add(book_id):
	current_member_id = member_controller.member_entity.get_identifier()
	library_catalog_controller.place_reservation(current_member_id, book_id)

	catalog_items = library_catalog_controller.fetch_catalog()
	member_controller.member_entity.configure_context(session, g)
	
	return render_template("books.html", msg="Book reserved", books=catalog_items, g=g)


@book_view.route('/books/search', methods=['GET'])
def search():
	member_controller.member_entity.configure_context(session, g)

	if "keyword" not in request.args:
		return render_template("search.html")

	search_query = request.args["keyword"]

	if len(search_query) < 1:
		return redirect('/books')

	matching_books = library_catalog_controller.query_books(search_query)

	if matching_books and len(matching_books) > 0:
		return render_template("books.html", search=True, books=matching_books, count=len(matching_books), keyword=escape(search_query), g=g)

	return render_template('books.html', error="No books found!", keyword=escape(search_query))