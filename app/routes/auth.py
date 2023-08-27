from flask import render_template, url_for, flash, redirect, request, jsonify, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User
from app import app, db
from sqlalchemy.exc import IntegrityError

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return jsonify({'result': 'error', 'response': f'Current user exists in db ', 'meta': {'code': 400}}), 400
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'result': 'OK', 'response': 'Signed up', 'meta': {'code': 201}}), 201
        except IntegrityError as e:
            actual_error_message = e.args[0]
            expected_error_message = f"Duplicate entry '{username}' for key 'user.username'"
            if expected_error_message in actual_error_message:
                db.session.rollback()
                return jsonify({'result': 'error', 'response': f'{username} exists in db ', 'meta': {'code': 400}}), 400

    return jsonify({'result': 'error', 'response': f'internal server error', 'meta': {'code': 500}}), 500


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'result': 'OK', 'response': 'Already authenticated', 'meta': {'code': 200}}), 200
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.password == request.form.get('password'):
            login_user(user)
            return jsonify({'result': 'OK', 'response': 'Authorised', 'meta': {'code': 200}}), 200
        else:
            return jsonify({'result': 'error', 'response': f'Login unsuccessful. Check your pass and username',
                            'meta': {'code': 400}}), 400


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'result': 'OK', 'response': 'Logout', 'meta': {'code': 200}}), 200