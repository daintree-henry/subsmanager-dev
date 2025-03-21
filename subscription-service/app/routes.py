from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta  # 새로 추가
from http import HTTPStatus

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import SubscriptionProvider, UserSubscription, SubscriptionPayment, SubscriptionPlan
from sqlalchemy.orm import joinedload

bp = Blueprint('api', __name__)

@bp.route('/sub', methods=['POST'])
@jwt_required()
def create_subscription():
    """
    새로운 구독을 생성하거나 비활성화된 구독을 재활성화하는 엔드포인트
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    current_app.logger.info(f'User {current_user_id} is attempting to create a subscription with data: {data}')

    try:
        required_fields = ['subscription_plan_id', 'start_date', 'payment_method']
        for field in required_fields:
            if field not in data:
                current_app.logger.warning(f'Missing required field: {field}')
                return jsonify({'error': f'Required field is missing: {field}'}), HTTPStatus.BAD_REQUEST

        subscription_plan = SubscriptionPlan.query.get(data['subscription_plan_id'])
        if not subscription_plan:
            current_app.logger.warning('Subscription plan not found.')
            return jsonify({'error': 'Subscription plan not found.'}), HTTPStatus.BAD_REQUEST

        # 사용자의 해당 플랜에 대한 구독 확인 (상태 무관)
        existing = UserSubscription.query.filter_by(
            user_id=current_user_id,
            subscription_plan_id=data['subscription_plan_id']
        ).first()

        if existing:
            if existing.status == 'active':
                current_app.logger.warning('User already has an active subscription.')
                return jsonify({'error': 'An active subscription already exists.'}), HTTPStatus.CONFLICT

            # 비활성 구독을 재활성화
            existing.status = 'active'
            existing.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            existing.payment_method = data['payment_method']
            existing.next_billing_date = existing.start_date + relativedelta(
                months=subscription_plan.billing_cycle_months
            )

            # 새로운 결제 기록 생성
            payment = SubscriptionPayment(
                user_subscription_id=existing.id,
                amount_paid=subscription_plan.monthly_fee * subscription_plan.billing_cycle_months,
                payment_status='successful',
                payment_method=existing.payment_method,
            )

            db.session.add(payment)
            db.session.commit()

            current_app.logger.info(f'Reactivated subscription {existing.id} for user {current_user_id}')
            return jsonify({
                'message': 'Subscription reactivated successfully.',
                'subscription': existing.to_dict()
            }), HTTPStatus.OK

        # 새로운 구독 생성
        subscription = UserSubscription(
            user_id=current_user_id,
            subscription_plan_id=data['subscription_plan_id'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            payment_method=data['payment_method'],
            status='active'
        )

        subscription.next_billing_date = subscription.start_date + relativedelta(
            months=subscription_plan.billing_cycle_months
        )

        db.session.add(subscription)
        db.session.flush()

        current_app.logger.info(f'Created subscription {subscription.id} for user {current_user_id}')

        payment = SubscriptionPayment(
            user_subscription_id=subscription.id,
            amount_paid=subscription_plan.monthly_fee * subscription_plan.billing_cycle_months,
            payment_status='successful',
            payment_method=subscription.payment_method,
        )

        db.session.add(payment)
        db.session.commit()

        current_app.logger.info(f'Payment record created for subscription {subscription.id}')
        return jsonify({
            'message': 'Subscription created successfully.',
            'subscription': subscription.to_dict()
        }), HTTPStatus.CREATED

    except ValueError as e:
        db.session.rollback()
        current_app.logger.error(f'ValueError occurred: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        current_app.logger.error(f'Error occurred while creating subscription: {str(e)}', exc_info=True)
        db.session.rollback()
        return jsonify({'error': 'A server error occurred.'}), HTTPStatus.INTERNAL_SERVER_ERROR

@bp.route('/sub/<int:subscription_id>', methods=['GET'])
@jwt_required()
def get_subscription(subscription_id):
    """
    특정 구독 정보를 조회하는 엔드포인트.
    """
    current_user_id = get_jwt_identity()
    current_app.logger.info(f'User {current_user_id} is requesting subscription {subscription_id}')

    try:
        subscription = UserSubscription.query.get(subscription_id)
        if not subscription:
            current_app.logger.warning(f'Subscription {subscription_id} not found.')
            return jsonify({'error': 'Subscription information not found.'}), HTTPStatus.NOT_FOUND

        if str(subscription.user_id) != current_user_id:
            current_app.logger.warning(
                f'Unauthorized access attempt: user_id={current_user_id}, subscription_id={subscription_id}')
            return jsonify({'error': 'Access denied.'}), HTTPStatus.FORBIDDEN

        return jsonify(subscription.to_dict()), HTTPStatus.OK

    except Exception as e:
        current_app.logger.error(f'Error occurred while retrieving subscription: {str(e)}', exc_info=True)
        return jsonify({'error': 'A server error occurred.'}), HTTPStatus.INTERNAL_SERVER_ERROR

@bp.route('/sub/plans', methods=['GET'])
@jwt_required()
def get_subscription_plans():
    """
    활성화된 구독 요금제 및 제공업체 정보를 조회하는 엔드포인트.
    """
    try:
        current_app.logger.info('Fetching all active subscription plans.')

        # SubscriptionPlan을 가져올 때 SubscriptionProvider 정보를 함께 로드
        plans = (
            SubscriptionPlan.query
            .filter_by(is_active=True)
            .options(joinedload(SubscriptionPlan.provider))  # SQLAlchemy ORM 조인
            .order_by(SubscriptionPlan.id.asc())  # 이름 기준 오름차순 정렬
            .all()
        )

        # JSON 응답으로 변환
        plan_list = [
            {
                "id": plan.id,
                "plan_name": plan.plan_name,
                "monthly_fee": float(plan.monthly_fee),
                "billing_cycle_months": plan.billing_cycle_months,
                "logo_file_name": plan.logo_file_name,
                "features": plan.features,
                "provider_name": plan.provider.provider_name,
                "created_at": plan.created_at.isoformat() if plan.created_at else None,
                "updated_at": plan.updated_at.isoformat() if plan.updated_at else None
            }
            for plan in plans
        ]

        return jsonify(plan_list), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching subscription plans: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/sub/plans/user', methods=['GET'])
@jwt_required()
def get_user_subscription_plans():
    """
    현재 로그인한 사용자의 구독 플랜 정보를 조회하는 엔드포인트
    """
    try:
        current_app.logger.info('Fetching user subscription plans')
        user_id = get_jwt_identity()

        # 사용자의 구독 정보 조회
        subscriptions = (
            UserSubscription.query
            .join(SubscriptionPlan)
            .join(SubscriptionProvider)
            .filter(UserSubscription.user_id == user_id)
            .filter(UserSubscription.status == 'active')
            .options(joinedload(UserSubscription.subscription_plan).joinedload(SubscriptionPlan.provider))
            .order_by(UserSubscription.id.asc())
            .all()
        )

        subscription_list = [
            {
                "subscription_id": sub.id,
                "start_date": sub.start_date.isoformat() if sub.start_date else None,
                "next_billing_date": sub.next_billing_date.isoformat() if sub.next_billing_date else None,
                "auto_renewal": sub.auto_renewal,
                "status": sub.status,
                "plan": {
                    "id": sub.subscription_plan.id,
                    "plan_name": sub.subscription_plan.plan_name,
                    "monthly_fee": float(sub.subscription_plan.monthly_fee),
                    "billing_cycle_months": sub.subscription_plan.billing_cycle_months,
                    "logo_file_name": sub.subscription_plan.logo_file_name,
                    "features": sub.subscription_plan.features,
                    "provider_name": sub.subscription_plan.provider.provider_name,
                },
                "created_at": sub.created_at.isoformat() if sub.created_at else None,
                "updated_at": sub.updated_at.isoformat() if sub.updated_at else None
            }
            for sub in subscriptions
        ]

        return jsonify(subscription_list), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching user subscription plans: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/sub/<int:subscription_id>/extend', methods=['POST'])
@jwt_required()
def extend_subscription(subscription_id):
    """
    사용자의 활성 구독을 연장하는 엔드포인트.
    """
    current_user_id = get_jwt_identity()
    current_app.logger.info(f'User {current_user_id} is attempting to extend subscription {subscription_id}')

    try:
        # 구독 정보 조회
        subscription = UserSubscription.query.get(subscription_id)
        if not subscription:
            current_app.logger.warning(f'Subscription {subscription_id} not found.')
            return jsonify({'error': 'Subscription not found.'}), HTTPStatus.NOT_FOUND

        # 사용자가 해당 구독의 소유자인지 확인
        if str(subscription.user_id) != current_user_id:
            current_app.logger.warning(f'Unauthorized access attempt by user {current_user_id} to extend subscription {subscription_id}')
            return jsonify({'error': 'Access denied.'}), HTTPStatus.FORBIDDEN

        # 이미 취소된 경우 연장 불가
        if subscription.status in ['cancelled', 'expired', 'suspended']:
            current_app.logger.info(f'Subscription {subscription_id} is {subscription.status} and cannot be extended.')
            return jsonify({'error': f'Cannot extend a {subscription.status} subscription.'}), HTTPStatus.BAD_REQUEST

        # 현재 결제 주기를 기준으로 연장
        extension_period = timedelta(days=30)  # 기본 한 달 연장 (구독 플랜에서 가져올 수도 있음)
        subscription.next_billing_date += extension_period
        subscription.updated_at = datetime.utcnow()
        db.session.commit()

        current_app.logger.info(f'Subscription {subscription_id} successfully extended.')
        return jsonify({'message': 'Subscription extended successfully.', 'new_billing_date': subscription.next_billing_date}), HTTPStatus.OK

    except Exception as e:
        current_app.logger.error(f'Error occurred while extending subscription: {str(e)}', exc_info=True)
        db.session.rollback()
        return jsonify({'error': 'A server error occurred.'}), HTTPStatus.INTERNAL_SERVER_ERROR

@bp.route('/sub/<int:subscription_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_subscription(subscription_id):
    """
    사용자의 활성 구독을 취소하는 엔드포인트.
    """
    current_user_id = get_jwt_identity()
    current_app.logger.info(f'User {current_user_id} is attempting to cancel subscription {subscription_id}')

    try:
        # 구독 정보 조회
        subscription = UserSubscription.query.get(subscription_id)
        if not subscription:
            current_app.logger.warning(f'Subscription {subscription_id} not found.')
            return jsonify({'error': 'Subscription not found.'}), HTTPStatus.NOT_FOUND

        # 사용자가 해당 구독의 소유자인지 확인
        if str(subscription.user_id) != current_user_id:
            current_app.logger.warning(f'Unauthorized access attempt by user {current_user_id} to cancel subscription {subscription_id}')
            return jsonify({'error': 'Access denied.'}), HTTPStatus.FORBIDDEN

        # 이미 취소된 경우
        if subscription.status == 'cancelled':
            current_app.logger.info(f'Subscription {subscription_id} is already canceled.')
            return jsonify({'message': 'Subscription is already canceled.'}), HTTPStatus.OK

        # 구독 상태 업데이트
        subscription.status = 'cancelled'
        subscription.updated_at = datetime.utcnow()
        db.session.commit()

        current_app.logger.info(f'Subscription {subscription_id} successfully canceled.')
        return jsonify({'message': 'Subscription canceled successfully.'}), HTTPStatus.OK

    except Exception as e:
        current_app.logger.error(f'Error occurred while canceling subscription: {str(e)}', exc_info=True)
        db.session.rollback()
        return jsonify({'error': 'A server error occurred.'}), HTTPStatus.INTERNAL_SERVER_ERROR

@bp.route('/sub/payments', methods=['POST'])
@jwt_required()
def create_subscription_payment():
    """
    구독 결제 정보를 생성하는 엔드포인트
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        # 필수 필드 검증
        required_fields = ['user_subscription_id', 'amount_paid', 'payment_method']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # UserSubscription 존재 여부 확인
        user_subscription = UserSubscription.query.get(data['user_subscription_id'])
        if not user_subscription:
            return jsonify({'error': 'User subscription not found'}), 404

        # 해당 사용자의 구독인지 확인
        if user_subscription.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access to subscription'}), 403

        # 결제 정보 생성
        payment = SubscriptionPayment(
            user_subscription_id=data['user_subscription_id'],
            amount_paid=data['amount_paid'],
            payment_method=data['payment_method'],
            payment_status='pending'  # 초기 상태는 pending으로 설정
        )

        db.session.add(payment)
        db.session.commit()

        current_app.logger.info(f'Created new subscription payment: {payment.id}')
        return jsonify(payment.to_dict()), 201

    except Exception as e:
        current_app.logger.error(f"Error creating subscription payment: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/sub/payments', methods=['GET'])
@jwt_required()
def get_user_payments():
    """
    현재 사용자의 모든 구독 결제 정보를 조회하는 엔드포인트
    """
    try:
        current_user_id = get_jwt_identity()

        # 페이지네이션 파라미터
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # 결제 상태 필터
        payment_status = request.args.get('status')

        subquery = (db.session.query(
            UserSubscription.id,
            SubscriptionPlan.plan_name,
            SubscriptionProvider.provider_name
        )
                    .join(SubscriptionPlan, UserSubscription.subscription_plan_id == SubscriptionPlan.id)
                    .join(SubscriptionProvider, SubscriptionPlan.provider_id == SubscriptionProvider.id)
                    .filter(UserSubscription.user_id == current_user_id)
                    .subquery())

        query = (db.session.query(
            SubscriptionPayment.id,
            subquery.c.plan_name,
            subquery.c.provider_name,
            SubscriptionPayment.amount_paid,
            SubscriptionPayment.payment_date,
            SubscriptionPayment.payment_status,
            SubscriptionPayment.payment_method
        )
                 .join(subquery, SubscriptionPayment.user_subscription_id == subquery.c.id))

        # 결제 상태 필터 적용
        if payment_status:
            query = query.filter(SubscriptionPayment.payment_status == payment_status)

        # 페이지네이션 적용
        paginated_query = query.order_by(SubscriptionPayment.payment_date.desc())
        page_items = paginated_query.paginate(page=page, per_page=per_page, error_out=False)

        # 응답 데이터 구성
        def format_payment(payment):
            return {
                'id': payment.id,
                'plan_name': payment.plan_name,
                'provider_name': payment.provider_name,
                'amount_paid': float(payment.amount_paid),
                'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
                'payment_status': payment.payment_status,
                'payment_method': payment.payment_method
            }

        response_data = {
            'items': [format_payment(payment) for payment in page_items.items],
            'total': page_items.total,
            'pages': page_items.pages,
            'current_page': page_items.page
        }

        current_app.logger.info(f'Successfully fetched payments for user {current_user_id}')
        return jsonify(response_data), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching user payments: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500