-- 1. 데이터베이스 생성
-- superuser로 접속하여 실행
CREATE DATABASE user_service
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

-- 데이터베이스 선택
\c user_service;

-- 2. users 테이블 생성
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) NOT NULL,
    username VARCHAR(80) NOT NULL,
    password_hash VARCHAR(256),
    full_name VARCHAR(120),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- 3. 이메일과 사용자명에 대한 유니크 인덱스 생성
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- 4. updated_at 자동 업데이트를 위한 트리거 함수
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- 5. updated_at 자동 업데이트 트리거 생성
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 6. 확인용 쿼리 (선택적으로 실행 가능)
-- 테이블 생성 확인
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

-- 트리거 생성 확인
SELECT tgname, tgrelid::regclass AS table_name
FROM pg_trigger
WHERE tgname = 'update_users_updated_at';

-- 7. 샘플 데이터 삽입
INSERT INTO users (email, username, password_hash, full_name, is_active)
VALUES
('john@subs.com', 'johndoe', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'John Doe', TRUE),
('jane@subs.com', 'janedoe', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'Jane Doe', TRUE),
('bob@subs.com', 'bobsmith', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'Bob Smith', TRUE),
('alice@subs.com', 'alicejones', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'Alice Jones', TRUE),
('charlie@subs.com', 'charliebrown', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'Charlie Brown', TRUE),
('david@subs.com', 'davidtaylor', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'David Taylor', TRUE),
('emma@subs.com', 'emmawilson', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'Emma Wilson', TRUE),
('frank@subs.com', 'frankthomas', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'Frank Thomas', TRUE),
('grace@subs.com', 'graceevans', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'Grace Evans', TRUE),
('henry@subs.com', 'henrymorgan', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'Henry Morgan', TRUE),
('isabella@subs.com', 'isabellalewis', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'Isabella Lewis', TRUE),
('jack@subs.com', 'jackmartin', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'Jack Martin', TRUE),
('karen@subs.com', 'karenlee', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'Karen Lee', TRUE),
('louis@subs.com', 'louishall', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'Louis Hall', TRUE),
('mia@subs.com', 'miaclark', 'scrypt:32768:8:1$TJgF3ln3IytxhAxa$1a93b0210042f1a3eeda3c22e73528b7ccb8fd08a1a2f9290211b4868d4ad6fb0dae917d7a8566da390c9a216e69e8ca7056a45d06f6a280a8127f2c100462a1', 'Mia Clark', TRUE);
