#打开文件涉及到的参数，open(name,mode,encoding)
#name代表是打开目标文件名的字符串（可以包含文件的具体路径）;mode设置打开文件的模式：只读，写入，追加等；encoding编码格式（推荐使用UTF8）
#mode模式r只读，w写入，a追加。
import pandas as pd

source_path = r"E:\编程学习\20260416.xlsx"
output_path = r"E:\编程学习\Programm learning\0905.xlsx"

major_columns = ["研究生专业", "本科专业", "大专专业"]

frames = []
excel_file = pd.ExcelFile(source_path)

for sheet_name in excel_file.sheet_names:
    df = pd.read_excel(source_path, sheet_name=sheet_name)

    mask = (
        df[major_columns]
        .fillna("")
        .astype(str)
        .apply(lambda col: col.str.contains("化学类|法学类", regex=True))
        .any(axis=1)
    )

    part = df[mask].copy()
    part["来源工作表"] = sheet_name
    frames.append(part)

result = pd.concat(frames, ignore_index=True)
result.to_excel(output_path, index=False)

print(f"已筛选 {len(result)} 条岗位信息，保存为：{output_path}")