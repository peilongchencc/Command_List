from module1 import MyClass as MyClass1
from module2 import MyClass as MyClass2

obj1 = MyClass1()
obj2 = MyClass2()

if isinstance(obj1, MyClass1):
    print("obj1 是 module1 中的 MyClass1 的实例")

if isinstance(obj2, MyClass2):
    print("obj2 是 module2 中的 MyClass2 的实例")

if isinstance(obj1, MyClass2):
    print("obj1 是 module2 中的 MyClass2 的实例")
else:
    print("类的定义虽然完全相同，但由于类的导入位置不同，判断结果也不同。")