from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response
from app import DAO
from Misc.functions import *

from Controllers.AdminController import AdminController
from Controllers.LibraryCatalogController import LibraryCatalogController
from Controllers.MemberController import MemberController

admin_view = Blueprint('admin_routes', __name__, template_folder='../templates/admin/', url_prefix='/admin')

library_catalog_controller = LibraryCatalogController(DAO)
member_controller = MemberController(DAO)
admin_controller = AdminController(DAO)


@admin_view.route('/', methods=['GET'])
@admin_controller.admin_account.login_required
def home():
	admin_controller.admin_account.configure_context(session, g)

	return render_template('admin/home.html', g=g)


@admin_view.route('/signin/', methods=['GET', 'POST'])
@admin_controller.admin_account.guest_only
def signin():
	g.bg = 1
	
	if request.method == 'POST':
		submission_form = request.form
		email_address = str(submission_form["email"])
		raw_password = str(submission_form["password"])

		if len(email_address) < 1 or len(raw_password) < 1:
			return render_template('admin/signin.html', error="Email and password are required")

		admin_record = admin_controller.authenticate_admin(email_address, compute_string_hash(raw_password))

		if admin_record and len(admin_record) > 0:
			session['admin'] = int(admin_record["admin_id"])

			return redirect("/admin")

		return render_template('admin/signin.html', error="Email or password incorrect")

	return render_template('admin/signin.html')


@admin_view.route('/signout/', methods=['GET'])
@admin_controller.admin_account.login_required
def signout():
	admin_controller.logout_admin()

	return redirect("/admin/", code=302)


@admin_view.route('/users/view/', methods=['GET'])
@admin_controller.admin_account.login_required
def users_view():
	admin_controller.admin_account.configure_context(session, g)

	current_admin_id = int(admin_controller.admin_account.get_identifier())
	admin_user = admin_controller.fetch_admin_by_id(current_admin_id)
	registered_members = admin_controller.retrieve_all_users()

	return render_template('users.html', g=g, admin=admin_user, users=registered_members)



@admin_view.route('/books/', methods=['GET'])
@admin_controller.admin_account.login_required
def books():
	admin_controller.admin_account.configure_context(session, g)

	current_admin_id = int(admin_controller.admin_account.get_identifier())
	admin_user = admin_controller.fetch_admin_by_id(current_admin_id)
	catalog_items = library_catalog_controller.fetch_catalog(is_available=0)

	return render_template('books/views.html', g=g, books=catalog_items, admin=admin_user)

@admin_view.route('/books/<int:book_id>')
@admin_controller.admin_account.login_required
def view_book(book_id):
	admin_controller.admin_account.configure_context(session, g)

	if book_id != None:
		target_book = library_catalog_controller.find_book_by_id(book_id)
		book_borrowers = member_controller.fetch_book_borrowers(book_id)

		print('----------------------------')
		print(book_borrowers)
		
		if target_book and len(target_book) < 1:
			return render_template('books/book_view.html', error="No book found!")

		return render_template("books/book_view.html", books=target_book, books_owners=book_borrowers, g=g)


@admin_view.route('/books/add', methods=['GET', 'POST'])
@admin_controller.admin_account.login_required
def book_add():
	admin_controller.admin_account.configure_context(session, g)
	
	return render_template('books/add.html', g=g)


@admin_view.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
@admin_controller.admin_account.login_required
def book_edit(book_id):
	admin_controller.admin_account.configure_context(session, g)

	if book_id != None:
		target_book = library_catalog_controller.find_book_by_id(book_id)

		if target_book and len(target_book) < 1:
			return render_template('edit.html', error="No book found!")

		return render_template("books/edit.html", book=target_book, g=g)
	
	return redirect('/books')

@admin_view.route('/books/delete/<int:book_id>', methods=['GET'])
@admin_controller.admin_account.login_required
def book_delete(book_id):
	parsed_book_id = int(book_id)

	if parsed_book_id is not None:
		library_catalog_controller.remove_book(parsed_book_id)
	
	return redirect('/admin/books/')


@admin_view.route('/books/search', methods=['GET'])
def search():
	admin_controller.admin_account.configure_context(session, g)

	if "keyword" not in request.args:
		return render_template("books/view.html")

	search_keyword = request.args["keyword"]

	if len(search_keyword) < 1:
		return redirect('/admin/books')

	current_admin_id = int(admin_controller.admin_account.get_identifier())
	admin_user = admin_controller.fetch_admin_by_id(current_admin_id)

	matching_catalog = library_catalog_controller.query_books(search_keyword, 0)

	if len(matching_catalog) > 0:
		return render_template("books/views.html", search=True, books=matching_catalog, count=len(matching_catalog), keyword=escape(search_keyword), g=g, admin=admin_user)

	return render_template('books/views.html', error="No books found!", keyword=escape(search_keyword))