import requests
import json

BASE_URL = 'http://localhost:5000'  # 필요시 주소 변경

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
    res = requests.post(f'{BASE_URL}/users/register', json=TEST_USER)
    print_response(res)
    if res.status_code == 201:
        print('✅ 사용자 등록 성공')
    else:
        print('❌ 사용자 등록 실패')

def login_user():
    print('[2] 로그인 시도...')
    payload = {
        'email': TEST_USER['email'],
        'password': TEST_USER['password']
    }
    res = requests.post(f'{BASE_URL}/users/login', json=payload)
    print_response(res)
    if res.status_code != 200:
        print('❌ 로그인 실패')
        return None
    print('✅ 로그인 성공')
    return res.json().get('access_token')

def get_user_info(token):
    print('[3] JWT로 사용자 정보 조회 시도...')
    headers = {
        'Authorization': f'Bearer {token}'
    }
    res = requests.get(f'{BASE_URL}/users/me', headers=headers)
    print_response(res)
    if res.status_code == 200:
        print('✅ 사용자 정보 조회 성공')
    else:
        print('❌ 사용자 정보 조회 실패')

if __name__ == '__main__':
    register_user()
    token = login_user()
    if token:
        get_user_info(token)
