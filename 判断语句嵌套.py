'''test case: requirement:公司发放礼物
1.必须是大于等于18岁小于30岁的成年人
2.同时入职时间需要满足大于两年，或者级别大于3才可以领取'''
age=int(input("输入年龄："))
year=int(input("请输入入职年限："))
if age>=18:
    print("成年人符合，继续判断")
    if age<30:
        print("年龄达标")
    if year>2:
        print('小于30岁的成年人且入职超过2年，满足条件，可以领取')
    elif int(input("请输入级别："))>3:
        print("级别大于3，也可以领取")
else:
    print(不符合条件)
