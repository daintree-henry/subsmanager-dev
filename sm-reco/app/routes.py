from flask import Blueprint, jsonify, current_app, request
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
import os
import random
from .config import Config
import json
from datetime import timedelta

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

        # force=true 여부 확인
        force_recommend = request.args.get('force', 'false').lower() == 'true'

        # 사용자별 캐시 확인
        user_cache_key = f"user:{current_user_id}:recommendation"
        if not force_recommend:
            cached_recommendation = current_app.redis.get(user_cache_key)
            if cached_recommendation:
                current_app.logger.info(f'Returned cached recommendation for user {current_user_id}')
                return jsonify({
                    'recommends': json.loads(cached_recommendation)
                }), HTTPStatus.OK
        else:
            current_app.logger.info(f'Force recommendation triggered by user {current_user_id}')

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

        # 전체 플랜 캐시 확인
        cached_all_plans = current_app.redis.get(Config.CACHE_KEY)
        if cached_all_plans:
            all_plans_list = json.loads(cached_all_plans)
        else:
            all_plans_response = requests.get(
                f'{os.getenv("SUB_URL")}/sub/plans',
                headers={'Authorization': access_token}
            )
            if all_plans_response.status_code != HTTPStatus.OK:
                return jsonify({
                    'error': 'Failed to fetch available subscription plans.'
                }), HTTPStatus.INTERNAL_SERVER_ERROR

            all_plans_list = all_plans_response.json()

            # 캐시에 저장
            current_app.redis.setex(
                Config.CACHE_KEY,
                timedelta(seconds=Config.SUBS_CACHE_TTL_SECOND),
                json.dumps(all_plans_list)
            )
            current_app.logger.info("Fetched subscription plans from API and cached them")

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

        # 무작위 추천 
        recommended_plans = random.sample(filtered_plans, min(int(Config.RECOMMEND_COUNT), len(filtered_plans)))

        # 사용자별 캐시에 추천 결과 저장
        current_app.redis.setex(
            user_cache_key,
            timedelta(seconds=Config.RECOMMEND_CACHE_TTL_SECOND),
            json.dumps(recommended_plans)
        )

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

@bp.route('/health', methods=['GET'])
def health_check():
    """
    서버 헬스체크용 엔드포인트
    """
    return jsonify({
        'status': 'ok',
        'message': 'Server is healthy.'
    }), HTTPStatus.OK
