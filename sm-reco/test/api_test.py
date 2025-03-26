import requests
import json

BASE_URL = 'http://localhost:5000'  # recommend 서버 주소
SUB_URL = 'http://localhost:5001'   # 구독 서비스 주소 (os.getenv("SUB_URL")와 일치해야 함)

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
    if res.status_code == 200:
        return res.json()['access_token']
    return None

def test_recommendation(token, force=False):
    print(f'[3] 구독 추천 테스트 요청... (force={force})')
    headers = {'Authorization': f'Bearer {token}'}
    url = f'{BASE_URL}/recommend'
    if force:
        url += '?force=true'
    res = requests.post(url, headers=headers)
    print_response(res)

if __name__ == '__main__':
    register_user()
    token = login_user()

    if token:
        # 1차 요청: 캐시 없음 → 추천 생성
        test_recommendation(token)

        # 2차 요청: 캐시 있음 → 캐시된 추천 사용
        test_recommendation(token)

        # 3차 요청: 강제 추천 → 캐시 무시하고 새로운 추천 생성
        test_recommendation(token, force=True)