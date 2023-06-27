from flask_restx import Namespace, Resource, fields
from ..model.user import User
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask import request

auth_namespace = Namespace('authuser', description = 'An API for authentication')
signup_model = auth_namespace.model('SignUpModel', {
    'id': fields.Integer(description='user identifier', required = True),
    'name': fields.String(description='username', required=True),
    'email':fields.String(description="User's email", required=True),
    'password': fields.String(description='user password', required=True)
})

login_model = auth_namespace.model('LoginModel', {
    'email': fields.String(description='user email', required=True),
    'password': fields.String(description="user's password", required=True)
})


@auth_namespace.route('/signup')
class UserSignup(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(signup_model)
    def post(self):
       
       data = request.get_json()
       name = data['name']
       email = data['email']
       password = data['password']

       filtered_user = User.query.filter_by(email=email).first()
       if filtered_user:
           return {'message':'User already exists'}, 409
       else:
           new_user = User(name=name, email=email, password=password)
           new_user.save()

           return new_user, HTTPStatus.CREATED

@auth_namespace.route('/login')
class LoginUser(Resource):
    @auth_namespace.expect(login_model)
    def post(self):

        data = request.get_json()
        email = data['email'] 
        password = data['password']    

        user_exist = User.query.filter_by(email=email).first()
        if (user_exist is not None) and (user_exist.password == password):
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)  

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }   

            return response, HTTPStatus.CREATED 
        else:
            invalid_error_msg = {"message": "Invalid Credentials"}
            return invalid_error_msg, HTTPStatus.UNAUTHORIZED
        
@auth_namespace.route('/refresh')
class refreshUserToken(Resource):
    @jwt_required()
    def get(self):


        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        refresh_token = create_refresh_token(identity=current_user)

        response = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return response, HTTPStatus.CREATED

@auth_namespace.route('/get_me')
class getUserInfo(Resource):
    @jwt_required()
    def get(self):

        current_user = get_jwt_identity()
        user_email = User.query.filter_by(email=current_user).first()
        user_name = user_email.name

        response = {
            'name': user_name,
            'email': user_email
        }

        return response, HTTPStatus.OK
    
    