FROM postgres:15.5-alpine

# 환경 변수 설정
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=asdf1234!

# SQL 초기화 스크립트 복사
COPY sqls/users.sql /docker-entrypoint-initdb.d/
COPY sqls/subs.sql /docker-entrypoint-initdb.d/

# 포트 설정
EXPOSE 5432
