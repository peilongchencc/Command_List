# import redis
# import json
# from redis_config import get_redis_connection

# # 创建Redis客户端连接
# r = get_redis_connection()
# # 清空redis
# r.flushall()

# my_dict = {'name': 'John', 'age': 30, 'score': {'chinese':87, 'math':99, 'english':92}}
# my_dict = str(my_dict)

# r.set("my_dict", my_dict)

import redis

# 建立到Redis服务器的连接
r = redis.Redis(host='localhost', port=6379, db=0)

# 创建一个Pipeline对象
pipe = r.pipeline()

# 在Pipeline中添加多个SET命令
pipe.get('key1')
pipe.get('key2')
pipe.get('key3')

# 执行Pipeline中的所有命令
result = pipe.execute()
for i in result:
    print(i.decode())