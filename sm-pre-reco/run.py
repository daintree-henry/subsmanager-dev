import os
import json
import random
import requests
from redis import Redis
from datetime import timedelta
from config import Config


def get_all_users():
    try:
        resp = requests.get(
            f'{Config.USER_URL}/users/internal',
            headers={"X-Internal-Secret": Config.INTERNAL_SECRET}
        )
        resp.raise_for_status()
        return [user['id'] for user in resp.json()]
    except Exception as e:
        print(f"[ERROR] 사용자 목록 조회 실패: {e}")
        return []


def get_user_subscriptions(user_id):
    try:
        resp = requests.get(
            f'{Config.SUB_URL}/sub/plans/user',
            headers={
                "X-Internal-User-ID": str(user_id),
                "X-Internal-Secret": Config.INTERNAL_SECRET
            }
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] 사용자 {user_id}의 구독 정보 조회 실패: {e}")
        return []


def get_all_plans():
    try:
        resp = requests.get(f'{Config.SUB_URL}/sub/plans')
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] 전체 플랜 조회 실패: {e}")
        return []


def recommend_plans(user_subs, all_plans):
    user_plan_ids = {sub['plan']['id'] for sub in user_subs}
    user_providers = {sub['plan']['provider_name'] for sub in user_subs}

    provider_plan_map = {}
    for plan in all_plans:
        if plan['id'] not in user_plan_ids and plan['provider_name'] not in user_providers:
            provider_plan_map.setdefault(plan['provider_name'], []).append(plan)

    filtered = [random.choice(plans) for plans in provider_plan_map.values()]
    if not filtered:
        return []
    return random.sample(filtered, min(int(Config.RECOMMEND_COUNT), len(filtered)))


def cache_recommendation(redis_client, user_id, recommends):
    key = f"user:{user_id}:recommendation"
    redis_client.setex(key, Config.RECOMMEND_CACHE_TTL_SECOND, json.dumps(recommends))


def main():
    print("[INFO] 추천 캐시 선생성 작업 시작")

    redis_client = Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        db=Config.REDIS_DB,
        password=Config.REDIS_PASSWORD,
        decode_responses=True
    )

    all_users = get_all_users()
    all_plans = get_all_plans()

    for user_id in all_users:
        user_subs = get_user_subscriptions(user_id)
        recommends = recommend_plans(user_subs, all_plans)
        if recommends:
            cache_recommendation(redis_client, user_id, recommends)
            print(f"[OK] user:{user_id} 추천 캐시 완료")
        else:
            print(f"[SKIP] user:{user_id} 추천 없음")

    print("[DONE] 추천 캐시 작업 완료")

    print("[CHECK] 전체 캐시 내용 조회 시작")
    for key in redis_client.scan_iter("user:*:recommendation"):
        value = redis_client.get(key)
        print(f"{key} → {value}")

if __name__ == '__main__':
    main()
