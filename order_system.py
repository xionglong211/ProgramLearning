import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# 菜单数据（菜品编号: [名称, 单价]）
MENU = {
    "1": ["宫保鸡丁", 38],
    "2": ["鱼香肉丝", 32],
    "3": ["麻婆豆腐", 28],
    "4": ["酸菜鱼", 58],
    "5": ["炒时蔬", 22],
    "6": ["米饭", 3]
}

# 订单数据：列表，每个元素为 [编号, 名称, 单价, 数量]
ORDER = []

# 数据文件
ORDER_FILE = "order.json"

class OrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("点餐软件")
        self.root.geometry("600x500")
        self.load_order()  # 尝试加载之前保存的订单

        # 创建界面
        self.create_widgets()
        self.refresh_order_display()

    def create_widgets(self):
        """创建界面组件"""
        # 顶部菜单显示区域
        tk.Label(self.root, text="菜单", font=("Arial", 16)).pack(pady=5)

        menu_frame = tk.Frame(self.root)
        menu_frame.pack()

        # 显示菜单表格
        for i, (code, (name, price)) in enumerate(MENU.items()):
            tk.Label(menu_frame, text=f"{code}. {name}", width=15, anchor='w').grid(row=i, column=0, padx=5, pady=2)
            tk.Label(menu_frame, text=f"￥{price}", width=8, anchor='e').grid(row=i, column=1, padx=5, pady=2)
            tk.Button(menu_frame, text="点此菜", command=lambda c=code: self.add_dish(c)).grid(row=i, column=2, padx=5, pady=2)

        # 操作按钮区域
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="查看订单", command=self.view_order).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="结账", command=self.checkout).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="清空订单", command=self.clear_order).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="保存订单", command=self.save_order).pack(side=tk.LEFT, padx=5)

        # 订单显示区域（列表）
        tk.Label(self.root, text="当前订单", font=("Arial", 14)).pack(pady=5)

        self.order_listbox = tk.Listbox(self.root, height=10, width=70)
        self.order_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        # 绑定双击事件删除菜品
        self.order_listbox.bind('<Double-Button-1>', self.remove_item)

    def add_dish(self, code):
        """添加菜品，弹出数量输入框"""
        name, price = MENU[code]
        qty_str = simpledialog.askstring("输入数量", f"请输入 {name} 的数量：", parent=self.root)
        if qty_str is None:
            return
        try:
            qty = int(qty_str)
            if qty <= 0:
                messagebox.showerror("错误", "数量必须为正整数")
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数")
            return

        # 查找是否已存在该菜品
        for item in ORDER:
            if item[0] == code:
                item[3] += qty
                self.refresh_order_display()
                messagebox.showinfo("成功", f"已增加 {qty} 份 {name}")
                return

        # 否则新增
        ORDER.append([code, name, price, qty])
        self.refresh_order_display()
        messagebox.showinfo("成功", f"已添加 {qty} 份 {name}")

    def refresh_order_display(self):
        """刷新订单列表显示"""
        self.order_listbox.delete(0, tk.END)
        total = 0
        for idx, (code, name, price, qty) in enumerate(ORDER):
            subtotal = price * qty
            total += subtotal
            self.order_listbox.insert(tk.END, f"{idx+1}. {name} x{qty}  ￥{price}  ￥{subtotal}")
        self.order_listbox.insert(tk.END, f"总计: ￥{total}")

    def view_order(self):
        """弹出窗口显示完整订单（可选，但已显示在列表）"""
        if not ORDER:
            messagebox.showinfo("订单", "当前订单为空")
        else:
            total = sum(item[2] * item[3] for item in ORDER)
            msg = "\n".join([f"{item[1]} x{item[3]}  ￥{item[2]*item[3]}" for item in ORDER])
            msg += f"\n\n总计: ￥{total}"
            messagebox.showinfo("订单详情", msg)

    def remove_item(self, event):
        """双击订单项删除该菜品"""
        selection = self.order_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if index >= len(ORDER):  # 最后一行是总计，不能删除
            return
        # 确认删除
        item = ORDER[index]
        if messagebox.askyesno("确认", f"确定要删除 {item[1]} x{item[3]} 吗？"):
            del ORDER[index]
            self.refresh_order_display()

    def checkout(self):
        """结账：计算总价，清空订单"""
        if not ORDER:
            messagebox.showinfo("结账", "订单为空，无需结账")
            return
        total = sum(item[2] * item[3] for item in ORDER)
        if messagebox.askyesno("结账", f"总计: ￥{total}\n确认结账吗？"):
            ORDER.clear()
            self.refresh_order_display()
            messagebox.showinfo("结账", "结账成功，感谢用餐！")

    def clear_order(self):
        """清空订单（不保存）"""
        if ORDER and messagebox.askyesno("清空", "确定要清空所有订单吗？"):
            ORDER.clear()
            self.refresh_order_display()

    def save_order(self):
        """保存订单到文件"""
        try:
            with open(ORDER_FILE, 'w', encoding='utf-8') as f:
                json.dump(ORDER, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("保存", "订单已保存到文件")
        except Exception as e:
            messagebox.showerror("保存失败", str(e))

    def load_order(self):
        """启动时加载之前保存的订单"""
        if os.path.exists(ORDER_FILE):
            try:
                with open(ORDER_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                ORDER.extend(data)
            except Exception as e:
                print("加载订单失败:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderApp(root)
    root.mainloop()