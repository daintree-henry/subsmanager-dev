from flask import Blueprint, jsonify, current_app, request
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
import os
import random
from .config import Config

bp = Blueprint('api', __name__)


@bp.route('/recommend', methods=['POST'])
@jwt_required()
def recommend_subscription_plan():
    """
    현재 사용자가 구독하지 않은 플랜 중에서 랜덤하게 하나를 추천하는 엔드포인트
    """
    try:
        current_user_id = get_jwt_identity()
        current_app.logger.info(f'Fetching subscription recommendation for user {current_user_id}')

        # 현재 사용자의 구독 플랜 조회 API 호출
        access_token = request.headers.get('Authorization')
        user_subscriptions_response = requests.get(
            f'{os.getenv("SUB_URL")}/sub/plans/user',
            headers={'Authorization': access_token}
        )

        if user_subscriptions_response.status_code != HTTPStatus.OK:
            return jsonify({
                'error': 'Failed to fetch user subscription plans.'
            }), HTTPStatus.INTERNAL_SERVER_ERROR

        user_subscriptions_list = user_subscriptions_response.json()
        user_subscriptions_ids = {sub['plan']['id'] for sub in user_subscriptions_list}
        user_subscribed_providers = {sub['plan']['provider_name'] for sub in user_subscriptions_list}

        # 모든 활성화된 구독 플랜 조회 API 호출
        all_plans_response = requests.get(
            f'{os.getenv("SUB_URL")}/sub/plans',
            headers={'Authorization': access_token}
        )

        if all_plans_response.status_code != HTTPStatus.OK:
            return jsonify({
                'error': 'Failed to fetch available subscription plans.'
            }), HTTPStatus.INTERNAL_SERVER_ERROR

        all_plans_list = all_plans_response.json()

        # 사용자가 구독하지 않은 플랜 필터링 (같은 provider_name 제외)
        provider_plan_map = {}
        for plan in all_plans_list:
            if plan['id'] not in user_subscriptions_ids and plan['provider_name'] not in user_subscribed_providers:
                if plan['provider_name'] not in provider_plan_map:
                    provider_plan_map[plan['provider_name']] = []
                provider_plan_map[plan['provider_name']].append(plan)

        # 각 provider에서 하나씩 랜덤 선택
        filtered_plans = [random.choice(plans) for plans in provider_plan_map.values()]

        if not filtered_plans:
            return jsonify({
                'message': 'No available subscription plans to recommend.'
            }), HTTPStatus.OK

        # 무작위 추천 (최대 3개 선택)
        recommended_plans = random.sample(filtered_plans, min(int(Config.RECOMMEND_COUNT), len(filtered_plans)))

        current_app.logger.info(
            f'Successfully recommended plans {[plan["id"] for plan in recommended_plans]} for user {current_user_id}')
        return jsonify({
            'recommends': recommended_plans
        }), HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(f'Error occurred while getting recommendation: {str(e)}', exc_info=True)
        return jsonify({
            'error': 'An error occurred while processing your request.'
        }), HTTPStatus.INTERNAL_SERVER_ERROR

