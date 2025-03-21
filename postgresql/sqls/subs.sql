-- 1. 데이터베이스 생성
CREATE DATABASE subs_service
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

-- 데이터베이스 선택
\c subs_service;

-- 2. 서비스 제공자 테이블 생성
CREATE TABLE subscription_providers (
    id SERIAL PRIMARY KEY,
    provider_name VARCHAR(100) NOT NULL UNIQUE,
    business_registration_number VARCHAR(20),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. 구독 플랜 테이블 생성
CREATE TABLE subscription_plans (
    id SERIAL PRIMARY KEY,
    provider_id INTEGER NOT NULL REFERENCES subscription_providers(id),
    plan_name VARCHAR(100) NOT NULL,
    monthly_fee DECIMAL(10,2) NOT NULL,
    billing_cycle_months INTEGER DEFAULT 1,
    features JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    logo_file_name VARCHAR(255),
    UNIQUE (provider_id, plan_name)
);

-- 4. 사용자의 구독 정보 테이블 생성
CREATE TABLE user_subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    subscription_plan_id INTEGER NOT NULL REFERENCES subscription_plans(id),
    start_date DATE NOT NULL,
    next_billing_date DATE NOT NULL,
    auto_renewal BOOLEAN DEFAULT TRUE,
    payment_method VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'cancelled', 'suspended', 'expired')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_user_subs_user_id ON user_subscriptions(user_id);
CREATE INDEX idx_user_subs_plan_id ON user_subscriptions(subscription_plan_id);

-- 5. 구독 결제 내역 테이블 생성
CREATE TABLE subscription_payments (
    id SERIAL PRIMARY KEY,
    user_subscription_id INTEGER NOT NULL REFERENCES user_subscriptions(id),
    amount_paid DECIMAL(10,2) NOT NULL,
    payment_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('successful', 'failed', 'pending', 'refunded')),
    payment_method VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_subscription_payments_user_sub_id ON subscription_payments(user_subscription_id);

INSERT INTO subscription_providers
(provider_name, business_registration_number, contact_email, contact_phone, status)
VALUES
('Netflix', '120-86-15721', 'business@netflix.co.kr', '02-1234-5678', 'active'),
('YouTube Premium', '220-81-62517', 'partner.kr@youtube.com', '02-2345-6789', 'active'),
('Spotify', '527-88-00907', 'partner.kr@spotify.com', '02-3456-7890', 'active'),
('Disney+', '120-87-00773', 'partner.kr@disneyplus.com', '02-4567-8901', 'active'),
('Coupang Play', '120-88-01234', 'partner@coupangplay.com', '02-5678-9012', 'active'),
('Apple Music', '120-89-02345', 'partner.kr@apple.com', '02-6789-0123', 'active'),
('Wavve', '138-81-45678', 'partner@wavve.com', '02-7890-1234', 'active'),
('Tving', '106-86-76543', 'partner@tving.com', '02-8901-2345', 'active'),
('Watcha', '211-87-98765', 'partner@watcha.com', '02-9012-3456', 'active'),
('Apple TV+', '120-89-02345', 'partner.kr@apple.com', '02-6789-0123', 'active');

INSERT INTO subscription_plans
(provider_id, plan_name, monthly_fee, billing_cycle_months, features, is_active, logo_file_name)
VALUES
-- Netflix Plans
(1, 'Basic with Ads', 6.99, 1, '{"resolution": "720p", "concurrent_streams": 1, "downloads": false, "ads": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'netflix_logo.png'),
(1, 'Standard', 15.49, 1, '{"resolution": "1080p", "concurrent_streams": 2, "downloads": true, "ads": false, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'netflix_logo.png'),
(1, 'Premium', 19.99, 1, '{"resolution": "4K+HDR", "concurrent_streams": 4, "downloads": true, "ads": false, "spatial_audio": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'netflix_logo.png'),

-- YouTube Premium Plans
(2, 'Individual', 13.99, 1, '{"ad_free": true, "background_play": true, "downloads": true, "youtube_music": true, "offline_mixtape": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'youtube_premium_logo.png'),
(2, 'Family', 22.99, 1, '{"ad_free": true, "background_play": true, "downloads": true, "youtube_music": true, "family_members": 5, "family_sharing": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'youtube_premium_logo.png'),
(2, 'Student', 7.49, 1, '{"ad_free": true, "background_play": true, "downloads": true, "youtube_music": true, "student_verification": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'youtube_premium_logo.png'),

-- Spotify Plans
(3, 'Individual', 10.99, 1, '{"ad_free": true, "offline_mode": true, "high_quality_audio": true, "playlist_sharing": true, "supported_devices": ["TV", "computer", "mobile", "tablet", "smart_speaker"]}', true, 'spotify_logo.png'),
(3, 'Duo', 14.99, 1, '{"ad_free": true, "offline_mode": true, "high_quality_audio": true, "accounts": 2, "duo_mix": true, "supported_devices": ["TV", "computer", "mobile", "tablet", "smart_speaker"]}', true, 'spotify_logo.png'),
(3, 'Family', 16.99, 1, '{"ad_free": true, "offline_mode": true, "high_quality_audio": true, "family_members": 6, "parental_controls": true, "family_mix": true, "supported_devices": ["TV", "computer", "mobile", "tablet", "smart_speaker"]}', true, 'spotify_logo.png'),
(3, 'Student', 5.99, 1, '{"ad_free": true, "offline_mode": true, "high_quality_audio": true, "student_verification": true, "supported_devices": ["TV", "computer", "mobile", "tablet", "smart_speaker"]}', true, 'spotify_logo.png'),

-- Disney+ Plans
(4, 'Standard with Ads', 7.99, 1, '{"resolution": "1080p", "concurrent_streams": 2, "downloads": false, "ads": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'disney_plus_logo.png'),
(4, 'Standard', 10.99, 1, '{"resolution": "1080p", "concurrent_streams": 2, "downloads": true, "ads": false, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'disney_plus_logo.png'),
(4, 'Premium', 13.99, 1, '{"resolution": "4K+HDR", "concurrent_streams": 4, "downloads": true, "ads": false, "dolby_atmos": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'disney_plus_logo.png'),

-- Coupang Play Plans
(5, 'Standard', 4.99, 1, '{"resolution": "1080p", "concurrent_streams": 2, "downloads": true, "wow_membership": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'coupang_play_logo.png'),

-- Apple Music Plans
(6, 'Voice', 4.99, 1, '{"ad_free": true, "siri_only": true, "supported_devices": ["apple_devices"]}', true, 'apple_music_logo.png'),
(6, 'Student', 5.99, 1, '{"ad_free": true, "offline_mode": true, "lossless_audio": true, "spatial_audio": true, "student_verification": true, "supported_devices": ["apple_devices"]}', true, 'apple_music_logo.png'),
(6, 'Individual', 10.99, 1, '{"ad_free": true, "offline_mode": true, "lossless_audio": true, "spatial_audio": true, "lyrics_view": true, "supported_devices": ["apple_devices"]}', true, 'apple_music_logo.png'),
(6, 'Family', 16.99, 1, '{"ad_free": true, "offline_mode": true, "lossless_audio": true, "spatial_audio": true, "family_members": 6, "lyrics_view": true, "supported_devices": ["apple_devices"]}', true, 'apple_music_logo.png'),

-- Wavve Plans
(7, 'Basic', 8.99, 1, '{"resolution": "720p", "concurrent_streams": 1, "downloads": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'wavve_logo.png'),
(7, 'Standard', 12.99, 1, '{"resolution": "1080p", "concurrent_streams": 2, "downloads": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'wavve_logo.png'),
(7, 'Premium', 15.99, 1, '{"resolution": "4K", "concurrent_streams": 4, "downloads": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'wavve_logo.png'),

-- Tving Plans
(8, 'Basic', 7.99, 1, '{"resolution": "720p", "concurrent_streams": 1, "downloads": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'tving_logo.png'),
(8, 'Standard', 12.99, 1, '{"resolution": "1080p", "concurrent_streams": 2, "downloads": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'tving_logo.png'),
(8, 'Premium', 15.99, 1, '{"resolution": "4K", "concurrent_streams": 4, "downloads": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'tving_logo.png'),

-- Watcha Plans
(9, 'Basic', 7.99, 1, '{"resolution": "720p", "concurrent_streams": 1, "downloads": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'watcha_logo.png'),
(9, 'Standard', 9.99, 1, '{"resolution": "1080p", "concurrent_streams": 2, "downloads": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'watcha_logo.png'),
(9, 'Premium', 13.99, 1, '{"resolution": "4K", "concurrent_streams": 4, "downloads": true, "supported_devices": ["TV", "computer", "mobile", "tablet"]}', true, 'watcha_logo.png'),

-- Apple TV+ Plans
(10, 'Standard', 9.99, 1, '{"resolution": "4K", "concurrent_streams": 6, "downloads": true, "spatial_audio": true, "dolby_vision": true, "dolby_atmos": true, "supported_devices": ["apple_devices"], "shared_with_family": true}', true, 'apple_tv_plus_logo.png');

-- Insert user subscription data
INSERT INTO user_subscriptions
(user_id, subscription_plan_id, start_date, next_billing_date, auto_renewal, payment_method, status)
VALUES
-- User 1: Netflix Premium + YouTube Premium Individual + Spotify Family
(1, 3, '2023-12-15', '2024-02-15', true, 'credit_card', 'active'),
(1, 4, '2024-01-01', '2024-02-01', true, 'credit_card', 'active'),
(1, 9, '2023-11-20', '2024-02-20', true, 'credit_card', 'active'),

-- User 2: Netflix Standard + Disney+ Standard
(2, 2, '2023-10-01', '2024-02-01', true, 'credit_card', 'active'),
(2, 12, '2023-12-25', '2024-02-25', true, 'credit_card', 'active'),

-- User 3: Multiple services user
(3, 3, '2023-09-15', '2024-02-15', true, 'credit_card', 'active'),
(3, 5, '2023-11-01', '2024-02-01', true, 'paypal', 'active'),
(3, 13, '2023-12-10', '2024-02-10', true, 'credit_card', 'active'),
(3, 20, '2024-01-05', '2024-02-05', true, 'credit_card', 'active'),

-- User 4: Budget conscious user with basic plans
(4, 1, '2023-12-01', '2024-02-01', true, 'credit_card', 'active'),
(4, 11, '2024-01-15', '2024-02-15', true, 'credit_card', 'active'),

-- User 5: Apple ecosystem user
(5, 19, '2023-11-01', '2024-02-01', true, 'apple_pay', 'active'),
(5, 27, '2023-12-15', '2024-02-15', true, 'apple_pay', 'active'),

-- User 6: Korean content focus
(6, 20, '2023-10-20', '2024-02-20', true, 'credit_card', 'active'),
(6, 23, '2023-11-15', '2024-02-15', true, 'credit_card', 'active'),
(6, 26, '2024-01-01', '2024-02-01', true, 'samsung_pay', 'active'),

-- User 7: Premium content user
(7, 3, '2023-09-01', '2024-02-01', true, 'credit_card', 'active'),
(7, 13, '2023-10-15', '2024-02-15', true, 'credit_card', 'active'),
(7, 22, '2023-12-01', '2024-02-01', true, 'credit_card', 'active'),

-- User 8: Music streaming focus
(8, 7, '2023-11-01', '2024-02-01', true, 'credit_card', 'active'),
(8, 18, '2023-12-15', '2024-02-15', true, 'apple_pay', 'active'),

-- User 9: Cancelled subscription
(9, 2, '2023-08-01', '2024-01-01', false, 'credit_card', 'cancelled'),
(9, 4, '2023-12-01', '2024-02-01', true, 'paypal', 'active'),

-- User 10: Student plans
(10, 6, '2023-12-01', '2024-02-01', true, 'credit_card', 'active'),
(10, 10, '2024-01-01', '2024-02-01', true, 'credit_card', 'active'),

-- User 11: Family plan user
(11, 5, '2023-11-15', '2024-02-15', true, 'credit_card', 'active'),
(11, 9, '2023-12-01', '2024-02-01', true, 'credit_card', 'active'),

-- User 12: Korean streaming services
(12, 20, '2023-10-01', '2024-02-01', true, 'credit_card', 'active'),
(12, 23, '2023-11-01', '2024-02-01', true, 'credit_card', 'active'),
(12, 26, '2023-12-01', '2024-02-01', true, 'kakao_pay', 'active'),

-- User 13: Mixed usage
(13, 2, '2023-12-15', '2024-02-15', true, 'credit_card', 'active'),
(13, 15, '2024-01-01', '2024-02-01', true, 'credit_card', 'active'),
(13, 20, '2023-11-01', '2024-02-01', true, 'naver_pay', 'active'),

-- User 14: Premium video services
(14, 3, '2023-11-15', '2024-02-15', true, 'credit_card', 'active'),
(14, 13, '2023-12-01', '2024-02-01', true, 'credit_card', 'active'),
(14, 22, '2024-01-01', '2024-02-01', true, 'samsung_pay', 'active'),

-- User 15: Basic plans user
(15, 1, '2023-12-01', '2024-02-01', true, 'credit_card', 'active'),
(15, 20, '2024-01-01', '2024-02-01', true, 'credit_card', 'active'),
(15, 26, '2023-11-15', '2024-02-15', true, 'kakao_pay', 'active');

-- Insert subscription payment data
INSERT INTO subscription_payments
(user_subscription_id, amount_paid, payment_date, payment_status, payment_method)
VALUES
-- User 1's payments (Netflix Premium, YouTube Premium Individual, Spotify Family)
(1, 19.99, '2023-12-15 10:30:00+09', 'successful', 'credit_card'),
(1, 19.99, '2024-01-15 10:30:00+09', 'successful', 'credit_card'),
(2, 13.99, '2024-01-01 09:00:00+09', 'successful', 'credit_card'),
(3, 16.99, '2023-11-20 14:20:00+09', 'successful', 'credit_card'),
(3, 16.99, '2023-12-20 14:20:00+09', 'successful', 'credit_card'),
(3, 16.99, '2024-01-20 14:20:00+09', 'successful', 'credit_card'),

-- User 2's payments (Netflix Standard, Disney+ Standard)
(4, 15.49, '2023-12-01 11:15:00+09', 'successful', 'credit_card'),
(4, 15.49, '2024-01-01 11:15:00+09', 'successful', 'credit_card'),
(5, 10.99, '2023-12-25 16:45:00+09', 'successful', 'credit_card'),
(5, 10.99, '2024-01-25 16:45:00+09', 'failed', 'credit_card'),
(5, 10.99, '2024-01-25 17:30:00+09', 'successful', 'credit_card'),

-- User 3's payments (Multiple services)
(6, 19.99, '2023-12-15 08:00:00+09', 'successful', 'credit_card'),
(6, 19.99, '2024-01-15 08:00:00+09', 'successful', 'credit_card'),
(7, 22.99, '2023-12-01 13:20:00+09', 'successful', 'paypal'),
(7, 22.99, '2024-01-01 13:20:00+09', 'successful', 'paypal'),
(8, 13.99, '2023-12-10 15:45:00+09', 'successful', 'credit_card'),
(8, 13.99, '2024-01-10 15:45:00+09', 'successful', 'credit_card'),
(9, 12.99, '2024-01-05 10:00:00+09', 'successful', 'credit_card'),

-- User 4's payments (Budget plans)
(10, 6.99, '2023-12-01 09:30:00+09', 'successful', 'credit_card'),
(10, 6.99, '2024-01-01 09:30:00+09', 'successful', 'credit_card'),
(11, 7.99, '2024-01-15 12:00:00+09', 'successful', 'credit_card'),

-- User 5's payments (Apple ecosystem)
(12, 8.99, '2023-12-01 14:15:00+09', 'successful', 'apple_pay'),
(12, 8.99, '2024-01-01 14:15:00+09', 'successful', 'apple_pay'),
(13, 13.99, '2023-12-15 11:30:00+09', 'successful', 'apple_pay'),
(13, 13.99, '2024-01-15 11:30:00+09', 'successful', 'apple_pay'),

-- User 6's payments (Korean content focus)
(14, 12.99, '2023-11-20 16:00:00+09', 'successful', 'credit_card'),
(14, 12.99, '2023-12-20 16:00:00+09', 'failed', 'credit_card'),
(14, 12.99, '2023-12-20 17:30:00+09', 'successful', 'credit_card'),
(14, 12.99, '2024-01-20 16:00:00+09', 'successful', 'credit_card'),
(15, 12.99, '2023-12-15 13:45:00+09', 'successful', 'credit_card'),
(15, 12.99, '2024-01-15 13:45:00+09', 'successful', 'credit_card'),
(16, 9.99, '2024-01-01 10:20:00+09', 'successful', 'samsung_pay'),

-- User 7's payments (Premium content)
(17, 19.99, '2023-12-01 15:30:00+09', 'successful', 'credit_card'),
(17, 19.99, '2024-01-01 15:30:00+09', 'successful', 'credit_card'),
(18, 13.99, '2023-12-15 12:40:00+09', 'successful', 'credit_card'),
(18, 13.99, '2024-01-15 12:40:00+09', 'successful', 'credit_card'),
(19, 7.99, '2024-01-01 09:15:00+09', 'successful', 'credit_card'),

-- User 8's payments (Music streaming)
(20, 10.99, '2023-12-01 11:00:00+09', 'successful', 'credit_card'),
(20, 10.99, '2024-01-01 11:00:00+09', 'successful', 'credit_card'),
(21, 16.99, '2023-12-15 14:30:00+09', 'successful', 'apple_pay'),
(21, 16.99, '2024-01-15 14:30:00+09', 'successful', 'apple_pay'),

-- User 9's payments (Including cancelled subscription)
(22, 15.49, '2023-11-01 10:45:00+09', 'successful', 'credit_card'),
(22, 15.49, '2023-12-01 10:45:00+09', 'successful', 'credit_card'),
(23, 13.99, '2023-12-01 13:00:00+09', 'successful', 'paypal'),
(23, 13.99, '2024-01-01 13:00:00+09', 'successful', 'paypal'),

-- User 10's payments (Student plans)
(24, 7.49, '2023-12-01 16:20:00+09', 'successful', 'credit_card'),
(24, 7.49, '2024-01-01 16:20:00+09', 'successful', 'credit_card'),
(25, 5.99, '2024-01-01 12:15:00+09', 'successful', 'credit_card'),

-- Additional payment records for remaining users...
-- User 11-15 recent payments
(26, 22.99, '2024-01-15 09:45:00+09', 'successful', 'credit_card'),
(27, 16.99, '2024-01-01 14:50:00+09', 'successful', 'credit_card'),
(28, 12.99, '2024-01-01 11:30:00+09', 'successful', 'credit_card'),
(29, 12.99, '2024-01-01 15:40:00+09', 'successful', 'credit_card'),
(30, 9.99, '2024-01-01 10:10:00+09', 'successful', 'kakao_pay'),
(31, 15.49, '2024-01-15 13:25:00+09', 'successful', 'credit_card'),
(32, 4.99, '2024-01-01 16:55:00+09', 'successful', 'credit_card'),
(33, 12.99, '2024-01-01 12:35:00+09', 'successful', 'naver_pay'),
(34, 19.99, '2024-01-15 10:25:00+09', 'successful', 'credit_card'),
(35, 13.99, '2024-01-01 15:15:00+09', 'successful', 'credit_card'),
(36, 7.99, '2024-01-01 11:50:00+09', 'successful', 'samsung_pay'),
(37, 6.99, '2024-01-01 14:40:00+09', 'failed', 'credit_card'),
(37, 6.99, '2024-01-01 16:10:00+09', 'successful', 'credit_card'),
(38, 12.99, '2024-01-01 09:20:00+09', 'successful', 'credit_card'),
(39, 9.99, '2024-01-15 12:45:00+09', 'successful', 'kakao_pay');