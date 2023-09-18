from redis_config import get_redis_connection
def main():
    r = get_redis_connection()
    # 从Redis中提取对象
    my_data = (r.get('my_dict')).decode()
    return my_data
my_dict_bytes = main()
print(my_dict_bytes)
print(type(my_dict_bytes))