import sympy as sym
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox


# Hàm vẽ đồ thị hàm số bất kỳ
def ve_do_thi():
    ham_so = ham_entry.get()

    try:
        # Chuyển hàm số từ chuỗi sang biểu thức sympy
        x = sym.Symbol('x')
        fx = sym.sympify(ham_so)

        # Xóa đồ thị cũ nếu có
        plt.clf()

        # Tạo mảng giá trị cho x và tính giá trị tương ứng của y
        x_vals = np.linspace(-10, 10, 400)
        f_lambda = sym.lambdify(x, fx, modules=["numpy"])
        y_vals = f_lambda(x_vals)

        # Vẽ đồ thị
        plt.plot(x_vals, y_vals, label=f'y = {ham_so}')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.title(f'Đồ thị của hàm số: y = {ham_so}')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.legend()
        plt.show()

    except Exception as e:
        messagebox.showerror("Lỗi", f"Hàm số không hợp lệ. Vui lòng nhập lại.\nChi tiết lỗi: {e}")


# Hàm tính đạo hàm bậc n, tích phân, cực trị của hàm số nhập vào
def tinh_toan():
    ham_so = ham_entry.get()
    bac_dao_ham = int(dao_ham_entry.get())  # Lấy bậc đạo hàm từ ô nhập

    try:
        # Chuyển chuỗi nhập vào thành biểu thức sympy
        x = sym.Symbol('x')
        fx = sym.sympify(ham_so)

        # Tính đạo hàm bậc n
        dh = sym.diff(fx, x, bac_dao_ham)

        # Tính tích phân
        tich_phan = sym.integrate(fx, (x, -6, 6))

        # Tìm nghiệm của đạo hàm bậc 1 (điểm cực trị tiềm năng)
        dh1 = sym.diff(fx, x)
        nghiem_cuc_tri = sym.solve(dh1, x)

        # Tìm loại cực trị (cực đại, cực tiểu)
        cuc_tri_info = ""
        cuc_dai_info = ""
        for nghiem in nghiem_cuc_tri:
            dh2 = sym.diff(dh1, x)
            gia_tri_dh2 = dh2.subs(x, nghiem)
            if gia_tri_dh2 > 0:
                cuc_tri_info += f"Điểm x = {nghiem}: Cực tiểu\n"
            elif gia_tri_dh2 < 0:
                cuc_tri_info += f"Điểm x = {nghiem}: Cực đại\n"
                cuc_dai_info += f"Điểm cực đại tại x = {nghiem}\n"
            else:
                cuc_tri_info += f"Điểm x = {nghiem}: Điểm yên ngựa\n"

        # Hiển thị kết quả
        dh_label.config(text=f"Đạo hàm bậc {bac_dao_ham}: {sym.pretty(dh)}")
        tp_label.config(text=f"Tích phân từ -6 đến 6: {tich_phan}")
        cuc_tri_label.config(text=f"Cực trị:\n{cuc_tri_info}")
        cuc_dai_label.config(text=f"Điểm cực đại:\n{cuc_dai_info}")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Hàm số hoặc bậc đạo hàm không hợp lệ. Vui lòng nhập lại.\nChi tiết lỗi: {e}")


# Hàm thoát chương trình
def thoat():
    root.quit()


# Giao diện GUI chính
root = Tk()
root.title("Ứng dụng Toán học")
root.geometry("500x500")  # Thiết lập kích thước cửa sổ
root.configure(bg="#f0f0f0")  # Đặt màu nền

# Tạo khung để bố trí các phần
frame = Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

# Label và Entry để người dùng nhập hàm số
ham_label = Label(frame, text="Nhập hàm số (ví dụ: sin(x), cos(x), x**3 + 2*x**2 + 1):", bg="#f0f0f0")
ham_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
ham_entry = Entry(frame, width=40)
ham_entry.grid(row=1, column=0, padx=10, pady=5)

# Label và Entry để người dùng nhập bậc đạo hàm
dao_ham_label = Label(frame, text="Nhập bậc đạo hàm (n):", bg="#f0f0f0")
dao_ham_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)
dao_ham_entry = Entry(frame, width=5)
dao_ham_entry.grid(row=3, column=0, padx=10, pady=5, sticky=W)

# Nút để vẽ đồ thị hàm số
ve_button = Button(frame, text="Vẽ đồ thị hàm số", command=ve_do_thi, bg="#87cefa")
ve_button.grid(row=4, column=0, padx=10, pady=10, sticky=W)

# Nút để tính đạo hàm, tích phân, cực trị
tinh_button = Button(frame, text="Tính đạo hàm, tích phân, cực trị", command=tinh_toan, bg="#87cefa")
tinh_button.grid(row=5, column=0, padx=10, pady=10, sticky=W)

# Label để hiển thị kết quả đạo hàm và tích phân
dh_label = Label(frame, text="Đạo hàm:", bg="#f0f0f0")
dh_label.grid(row=6, column=0, padx=10, pady=5, sticky=W)

tp_label = Label(frame, text="Tích phân từ -6 đến 6:", bg="#f0f0f0")
tp_label.grid(row=7, column=0, padx=10, pady=5, sticky=W)

cuc_tri_label = Label(frame, text="Cực trị:", bg="#f0f0f0")
cuc_tri_label.grid(row=8, column=0, padx=10, pady=5, sticky=W)

cuc_dai_label = Label(frame, text="Điểm cực đại:", bg="#f0f0f0")
cuc_dai_label.grid(row=9, column=0, padx=10, pady=5, sticky=W)

# Nút để thoát chương trình
thoat_button = Button(root, text="Thoát", command=thoat, bg="#ff4500", fg="white")
thoat_button.pack(pady=20)

# Chạy giao diện
root.mainloop()
