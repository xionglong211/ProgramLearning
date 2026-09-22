#if elif else语句
#if 满足条件1执行
#elif 不满足条件1，但满足条件2执行
#elif 以上都不满足，满足条件3执行
#…………
#else 所有条件不满足执行
"""print("欢迎来到黑马动物园")
height=int(input("请输入你的身高（cm）："))
vip_level=int(input("请输入你的VIP级别（1~5）:"))
if height<=130:
    print("您的身高小于130cm，可以免费游玩。")
elif vip_level>=3:
    print("您符合免费入园条件。")
else:
    print("您不符合入园条件")"""
num=10#赋予一个变量值
if int(input("请输入第一次猜想的数字："))==num:#输入值与变量值比较
    print("恭喜你第一次猜对了")
elif int(input("不对，再猜一次："))==num:
    print("恭喜你猜对了")
elif int(input("不对，再猜最后一次："))==num:
    print("恭喜答对了1")
else:
    print("sorry,全部猜错了，我想的是：10")
