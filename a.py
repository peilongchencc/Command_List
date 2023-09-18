from typing import List

def sum_numbers(numbers: List[int]) -> int:
    return sum(numbers)

# numbers_list = [1, 2, 3, 4, 5]
numbers_list = [1, 2, 3, 4, '5']
result = sum_numbers(numbers_list)
print(result)