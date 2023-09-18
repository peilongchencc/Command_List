import redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# 创建Redis连接池
pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# 获取Redis连接
def get_redis_connection():
    return redis.Redis(connection_pool=pool)

# # 从Redis中获取数据的示例函数
# def get_data_from_redis(key):
#     redis_conn = get_redis_connection()
#     data = redis_conn.get(key)
#     return data

# def main():
#     key = 'your_key'
#     data = get_data_from_redis(key)
#     if data:
#         print(f'Data from Redis: {data.decode("utf-8")}')
#     else:
#         print('Data not found in Redis.')

# if __name__ == '__main__':
#     main()