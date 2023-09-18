import redis
import pickle

# 连接到Redis
r = redis.Redis(host='localhost', port=6379)

class MyClass:
    class_variable = 0

    def __init__(self, value):
        self.value = value

    @classmethod
    def class_method(cls, x):
        # cls参数指向类本身
        cls.class_variable += x

    def instance_method(self, y):
        # self参数指向实例
        self.value += y

# 调用类方法，不需要创建实例
MyClass.class_method(5)
# MyClass.class_variable  # 5
my_object = MyClass(12)

my_object_bytes = pickle.dumps(my_object)
r.set('my_object', my_object_bytes)