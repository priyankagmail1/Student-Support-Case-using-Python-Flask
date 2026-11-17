from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response, flash
from app import DAO
from Misc.functions import *

from Controllers.MemberController import MemberController

member_view = Blueprint('user_routes', __name__, template_folder='/templates')

member_controller = MemberController(DAO)


@member_view.route('/', methods=['GET'])
def home():
	g.bg = 1

	member_controller.member_entity.configure_context(session, g)
	print(g.user)

	return render_template('home.html', g=g)


@member_view.route('/signin', methods=['GET', 'POST'])
@member_controller.member_entity.guest_only
def signin():
	if request.method == 'POST':
		submission_form = request.form
		email_address = str(submission_form["email"])
		raw_password = str(submission_form["password"])

		if len(email_address) < 1 or len(raw_password) < 1:
			return render_template('signin.html', error="Email and password are required")

		member_record = member_controller.authenticate_member(email_address, compute_string_hash(raw_password))

		if member_record and len(member_record) > 0:
			session['user'] = int(member_record['id'])

			return redirect("/")

		return render_template('signin.html', error="Email or password incorrect")


	return render_template('signin.html')


@member_view.route('/signup', methods=['GET', 'POST'])
@member_controller.member_entity.guest_only
def signup():
	if request.method == 'POST':
		full_name = request.form.get('name')
		email_address = request.form.get('email')
		raw_password = request.form.get('password')

		if len(full_name) < 1 or len(email_address) < 1 or len(raw_password) < 1:
			return render_template('signup.html', error="All fields are required")

		created_member = member_controller.register_member(full_name, email_address, compute_string_hash(raw_password))

		if created_member == "already_exists":
			return render_template('signup.html', error="User already exists with this email")


		return render_template('signup.html', msg="You've been registered!")


	return render_template('signup.html')


@member_view.route('/signout/', methods=['GET'])
@member_controller.member_entity.auth_required
def signout():
	member_controller.logout_member()

	return redirect("/", code=302)

@member_view.route('/user/', methods=['GET'])
@member_controller.member_entity.auth_required
def show_user(member_id=None):
	member_controller.member_entity.configure_context(session, g)
	
	if member_id is None:
		member_id = int(member_controller.member_entity.get_identifier())

	member_record = member_controller.find_member_by_id(member_id)
	borrowed_books = member_controller.fetch_member_borrowed_books(member_id)

	return render_template("profile.html", user=member_record, books=borrowed_books, g=g)

@member_view.route('/user', methods=['POST'])
@member_controller.member_entity.auth_required
def update():
	member_controller.member_entity.configure_context(session, g)
	
	submission_form = request.form
	full_name = str(submission_form["name"])
	email_address = str(submission_form["email"])
	raw_password = str(submission_form["password"])
	profile_bio = str(submission_form["bio"])

	member_controller.modify_member_details(full_name, email_address, compute_string_hash(raw_password), profile_bio, member_controller.member_entity.get_identifier())

	flash('Your info has been updated!')
	return redirect("/user/")
