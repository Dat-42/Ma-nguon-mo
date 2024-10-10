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

# Label và Entry để người dùng nhập hàm số
ham_label = Label(root, text="Nhập hàm số (ví dụ: sin(x), cos(x), x**3 + 2*x**2 + 1):")
ham_label.pack(pady=5)
ham_entry = Entry(root, width=50)
ham_entry.pack(pady=5)

# Label và Entry để người dùng nhập bậc đạo hàm
dao_ham_label = Label(root, text="Nhập bậc đạo hàm (n):")
dao_ham_label.pack(pady=5)
dao_ham_entry = Entry(root, width=5)
dao_ham_entry.pack(pady=5)

# Nút để vẽ đồ thị hàm số
ve_button = Button(root, text="Vẽ đồ thị hàm số", command=ve_do_thi)
ve_button.pack(pady=5)

# Nút để tính đạo hàm, tích phân, cực trị
tinh_button = Button(root, text="Tính đạo hàm, tích phân, cực trị", command=tinh_toan)
tinh_button.pack(pady=5)

# Label để hiển thị kết quả đạo hàm và tích phân
dh_label = Label(root, text="Đạo hàm:")
dh_label.pack(pady=5)

tp_label = Label(root, text="Tích phân từ -6 đến 6:")
tp_label.pack(pady=5)

cuc_tri_label = Label(root, text="Cực trị:")
cuc_tri_label.pack(pady=5)

cuc_dai_label = Label(root, text="Điểm cực đại:")
cuc_dai_label.pack(pady=5)

# Nút để thoát chương trình
thoat_button = Button(root, text="Thoát", command=thoat)
thoat_button.pack(pady=5)

# Chạy giao diện
root.mainloop()
