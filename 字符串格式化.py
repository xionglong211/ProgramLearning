#f “内容{占位符} 代表的是字符串格式化的表达式
name="平安电工"
up_date="2026.06.06"
stock_prices=20.0
print("公司名称：",name, "上市日期：",up_date, "股票价格：",stock_prices)#方案1，逗号隔开
print(f"公司名称：{name},上市日期：{up_date},股票价格:{stock_prices}")#方案2，变量格式化{}不在乎变量格式
#print(f"{name},{Date},{prices}")