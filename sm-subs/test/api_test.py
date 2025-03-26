import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000'
TEST_USER = {
    'email': 'test@subs.com',
    'username': 'test',
    'password': 'testpass123',
    'full_name': '테스트사용자'
}

def print_response(res):
    print(f'📡 요청 URL: {res.request.method} {res.request.url}')
    if res.request.body:
        try:
            body = json.loads(res.request.body)
            print(f'📤 요청 바디: {json.dumps(body, indent=2, ensure_ascii=False)}')
        except:
            print(f'📤 요청 바디(raw): {res.request.body}')
    print(f'📥 응답 코드: {res.status_code}')
    try:
        print(f'📥 응답 바디: {json.dumps(res.json(), indent=2, ensure_ascii=False)}')
    except:
        print(f'📥 응답 바디(raw): {res.text}')
    print('—' * 60)

def register_user():
    print('[1] 사용자 등록 시도...')
    res = requests.post(f'http://sm-user:5000/users/register', json=TEST_USER)
    print_response(res)

def login_user():
    print('[2] 로그인 시도...')
    payload = {
        'email': TEST_USER['email'],
        'password': TEST_USER['password']
    }
    res = requests.post(f'http://sm-user:5000/users/login', json=payload)
    print_response(res)
    return res.json().get('access_token') if res.status_code == 200 else None

def get_headers(token):
    return {'Authorization': f'Bearer {token}'}

def fetch_plans(token):
    print('[3] 구독 요금제 조회...')
    res = requests.get(f'{BASE_URL}/sub/plans', headers=get_headers(token))
    print_response(res)
    if res.status_code == 200 and res.json():
        return res.json()[0]['id']  # 첫 요금제 ID 리턴
    return None

def create_subscription(token, plan_id):
    print('[4] 구독 생성 요청...')
    payload = {
        'subscription_plan_id': plan_id,
        'start_date': datetime.now().strftime('%Y-%m-%d'),
        'payment_method': 'credit_card'
    }
    res = requests.post(f'{BASE_URL}/sub', json=payload, headers=get_headers(token))
    print_response(res)
    if res.status_code in (200, 201):
        return res.json()['subscription']['id']
    return None

def extend_subscription(token, subscription_id):
    print('[5] 구독 연장 요청...')
    res = requests.post(f'{BASE_URL}/sub/{subscription_id}/extend', headers=get_headers(token))
    print_response(res)

def get_user_subscriptions(token):
    print('[6] 사용자 구독 목록 조회...')
    res = requests.get(f'{BASE_URL}/sub/plans/user', headers=get_headers(token))
    print_response(res)

def create_payment(token, subscription_id):
    print('[7] 결제 생성 요청...')
    payload = {
        'user_subscription_id': subscription_id,
        'amount_paid': 10000,
        'payment_method': 'credit_card'
    }
    res = requests.post(f'{BASE_URL}/sub/payments', json=payload, headers=get_headers(token))
    print_response(res)

def fetch_payments(token):
    print('[8] 사용자 결제 내역 조회...')
    res = requests.get(f'{BASE_URL}/sub/payments', headers=get_headers(token))
    print_response(res)

def cancel_subscription(token, subscription_id):
    print('[9] 구독 취소 요청...')
    res = requests.post(f'{BASE_URL}/sub/{subscription_id}/cancel', headers=get_headers(token))
    print_response(res)

if __name__ == '__main__':
    register_user()
    token = login_user()

    if token:
        plan_id = fetch_plans(token)
        if plan_id:
            sub_id = create_subscription(token, plan_id)
            if sub_id:
                extend_subscription(token, sub_id)
                get_user_subscriptions(token)
                create_payment(token, sub_id)
                fetch_payments(token)
                cancel_subscription(token, sub_id)
