"""
測試 class怎麼寫 和init的用法
"""

class task_test():

    def __init__(self) -> None:
        super().__init__()
        self.int1 = 1
        self.int2 = 100
        self.int3 = 1000
        self.int3 = 2

    def task1(self):
        ans =  self.int1 + self.int3
        return ans
    # def task3():
    #     pass
    
    # def task2():
    #     pass

    # def task4():
    #     pass

use_class = task_test()
print(use_class.task1())