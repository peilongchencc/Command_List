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