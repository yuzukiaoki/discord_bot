"""
測試 args* kawargs** 用法
"""

def hehe (a,*b,**c):
    print(f"hi I am {a} ")
    a_list=[]
    for arg in b:
        print(f"你是有幾個{arg}")
        a_list.append(arg)
    print(a_list)
    for one,two in c.items():
        print(f"這是{one}, 這是{two}")
    # print(c)
    # print(type(c))

# hehe("北七",4,5,6,"hehe","想不到吧",sam=87,jam=69,godtone=7414)
hehe("北七",4,5,6,"hehe","想不到吧",sam=87,jam=69,godtone=7414)