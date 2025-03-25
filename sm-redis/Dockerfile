FROM redis:8.0-M04

COPY redis.conf /usr/local/etc/redis/redis.conf

# 포트 설정
EXPOSE 6379

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
