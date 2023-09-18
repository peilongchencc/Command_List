import time

# 定义timing_decorator装饰器
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()              # 起始时间
        result = func(*args, **kwargs)        # 函数执行，函数有多个返回值依旧可以执行
        end_time = time.time()                # 结束时间
        elapsed_time = end_time - start_time  # 计算耗时
        
        # 根据不同情况获取名称
        # 对于函数来说，使用 `func.__name__` 可以获得函数名称；但对于类的实例，需要使用 `func.__class__.__name__` 来获得实例对应的类的名称。
        func_name = getattr(func, "__name__", None) or func.__class__.__name__
        
        print(f"Function {func_name} took {elapsed_time:.6f} seconds to execute.")
        return result
    return wrapper