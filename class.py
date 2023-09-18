import redis

# 创建一个Redis连接
r = redis.Redis(host='localhost', port=6379, db=0)
# 清空redis
r.flushall()

# 指定键名
key = 'xxxx'

# 尝试从Redis中获取数据，如果不存在则返回默认值
# data = r.get(key) or 'default_value'
data = r.get(key)

print(data)

# result = ["xxx", None, 777]
# result[0] = result[0] if result[0] is not None else  []
# result[1] = result[1] if result[1] is not None else  {}
# result[2] = result[2] if result[2] is not None else  {}
# print(result)