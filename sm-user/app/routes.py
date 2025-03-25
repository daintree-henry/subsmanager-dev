from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from http import HTTPStatus

from app import db, jwt
from app.models import User

bp = Blueprint('api', __name__)


@bp.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email is already registered.'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username is already in use.'}), 400

    user = User(
        email=data['email'],
        username=data['username'],
        full_name=data.get('full_name', '')
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@bp.route('/users/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Please enter both email and password.'}), 400

        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials.'}), 401

        additional_claims = {
            'email': user.email,
        }
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims,
            expires_delta=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        )

        return jsonify({
            'access_token': access_token,
            'user': user.to_dict(),
            'token_type': 'bearer'
        }), 200

    except Exception as e:
        # Log the error here
        return jsonify({'error': 'A server error occurred.'}), 500


@bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found.'}), 404

        # Add proper error handling for JWT-specific exceptions
        return jsonify(user.to_dict()), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired.'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token.'}), 401
    except Exception as e:
        # Add detailed logging for debugging
        return jsonify({'error': 'A server error occurred.'}), 500

@bp.route('/health', methods=['GET'])
def health_check():
    """
    서버 헬스체크용 엔드포인트
    """
    return jsonify({
        'status': 'ok',
        'message': 'Server is healthy.'
    }), HTTPStatus.OK