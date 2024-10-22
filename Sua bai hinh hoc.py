import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import math

# Hàm kiểm tra điều kiện tam giác
def kiem_tra_tam_giac(a, b, c):
    return a + b > c and a + c > b and b + c > a

# Hàm tính diện tích và chu vi cho hình 2D
def tinh_hinh_2d():
    try:
        selected_shape = combo_2d.get()
        if selected_shape == "Hình tròn":
            r = float(entry_ban_kinh.get())
            if r <= 0:
                raise ValueError("Bán kính phải lớn hơn 0.")
            dien_tich = math.pi * r ** 2
            chu_vi = 2 * math.pi * r
            messagebox.showinfo("Kết quả", f"Chu vi: {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")

        elif selected_shape == "Tam giác":
            a = float(entry_canh_1.get())
            b = float(entry_canh_2.get())
            c = float(entry_canh_3.get())
            if a <= 0 or b <= 0 or c <= 0:
                raise ValueError("Các cạnh phải lớn hơn 0.")
            if not kiem_tra_tam_giac(a, b, c):
                raise ValueError("Các cạnh không tạo thành một tam giác.")
            s = (a + b + c) / 2
            dien_tich = math.sqrt(s * (s - a) * (s - b) * (s - c))
            chu_vi = a + b + c
            messagebox.showinfo("Kết quả", f"Chu vi: {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")

        elif selected_shape == "Tứ giác":
            a = float(entry_canh_1.get())
            b = float(entry_canh_2.get())
            c = float(entry_canh_3.get())
            d = float(entry_canh_4.get())
            if a <= 0 or b <= 0 or c <= 0 or d <= 0:
                raise ValueError("Các cạnh phải lớn hơn 0.")
            chu_vi = a + b + c + d
            # Công thức tính diện tích hình tứ giác, ví dụ bằng công thức Bretschneider
            s = (a + b + c + d) / 2
            dien_tich = math.sqrt((s - a) * (s - b) * (s - c) * (s - d))
            messagebox.showinfo("Kết quả", f"Chu vi: {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")

        elif selected_shape == "Hình thang":
            a = float(entry_canh_1.get())
            b = float(entry_canh_2.get())
            h = float(entry_chieu_cao.get())
            if a <= 0 or b <= 0 or h <= 0:
                raise ValueError("Cạnh và chiều cao phải lớn hơn 0.")
            dien_tich = ((a + b) / 2) * h
            chu_vi = a + b + 2 * h  # Công thức giả định, cần điều chỉnh theo cụ thể
            messagebox.showinfo("Kết quả", f"Chu vi: {chu_vi:.2f}\nDiện tích: {dien_tich:.2f}")

    except ValueError as e:
        messagebox.showerror("Lỗi", f"Giá trị không hợp lệ: {e}")

# Hàm vẽ hình 2D
def ve_hinh_2d():
    try:
        selected_shape = combo_2d.get()
        if selected_shape == "Hình tròn":
            r = float(entry_ban_kinh.get())
            if r <= 0:
                raise ValueError("Bán kính phải lớn hơn 0.")
            plt.figure()
            circle = plt.Circle((0, 0), r, color='blue', fill=True, alpha=0.5)
            plt.gca().add_artist(circle)
            plt.xlim(-r - 1, r + 1)
            plt.ylim(-r - 1, r + 1)
            plt.title(f"Hình tròn với bán kính {r}")
            plt.gca().set_aspect('equal')
            plt.show()

        elif selected_shape == "Tam giác":
            a = float(entry_canh_1.get())
            b = float(entry_canh_2.get())
            c = float(entry_canh_3.get())
            if a <= 0 or b <= 0 or c <= 0:
                raise ValueError("Các cạnh phải lớn hơn 0.")
            if not kiem_tra_tam_giac(a, b, c):
                raise ValueError("Các cạnh không tạo thành một tam giác.")
            plt.figure()
            # Sử dụng công thức tính diện tích để tính chiều cao
            s = (a + b + c) / 2
            h = (2 * math.sqrt(s * (s - a) * (s - b) * (s - c))) / a
            plt.plot([0, b, c], [0, 0, h], 'bo-')  # Vẽ tam giác
            plt.fill([0, b, c], [0, 0, h], 'cyan', alpha=0.5)
            plt.xlim(-1, max(b, c) + 1)
            plt.ylim(-1, h + 1)
            plt.title(f"Tam giác với cạnh {a}, {b}, {c}")
            plt.gca().set_aspect('equal')
            plt.show()

        elif selected_shape == "Tứ giác":
            a = float(entry_canh_1.get())
            b = float(entry_canh_2.get())
            c = float(entry_canh_3.get())
            d = float(entry_canh_4.get())
            if a <= 0 or b <= 0 or c <= 0 or d <= 0:
                raise ValueError("Các cạnh phải lớn hơn 0.")
            plt.figure()
            # Giả định vẽ hình tứ giác (có thể là hình chữ nhật)
            plt.plot([0, a, a, 0, 0], [0, 0, b, b, 0], 'bo-')
            plt.fill([0, a, a, 0], [0, 0, b, b], 'cyan', alpha=0.5)
            plt.xlim(-1, a + 1)
            plt.ylim(-1, b + 1)
            plt.title(f"Tứ giác với các cạnh {a}, {b}, {c}, {d}")
            plt.gca().set_aspect('equal')
            plt.show()

        elif selected_shape == "Hình thang":
            a = float(entry_canh_1.get())
            b = float(entry_canh_2.get())
            h = float(entry_chieu_cao.get())
            if a <= 0 or b <= 0 or h <= 0:
                raise ValueError("Cạnh và chiều cao phải lớn hơn 0.")
            plt.figure()
            # Giả định vẽ hình thang
            plt.plot([0, a, b, 0], [0, h, h, 0], 'bo-')
            plt.fill([0, a, b, 0], [0, h, h, 0], 'cyan', alpha=0.5)
            plt.xlim(-1, max(a, b) + 1)
            plt.ylim(-1, h + 1)
            plt.title(f"Hình thang với cạnh {a}, {b} và chiều cao {h}")
            plt.gca().set_aspect('equal')
            plt.show()

    except ValueError as e:
        messagebox.showerror("Lỗi", f"Giá trị không hợp lệ: {e}")

def ve_hinh_3d():
    try:
        selected_shape = combo_3d.get()
        a = float(entry_canh_luc_giac.get())
        h = float(entry_chieu_cao.get())

        if a <= 0 or h <= 0:
            raise ValueError("Cạnh và chiều cao phải lớn hơn 0.")

        if selected_shape == "Hình trụ":
            dien_tich_xung_quanh = 2 * math.pi * a * h
            dien_tich_toan_phan = dien_tich_xung_quanh + 2 * math.pi * a ** 2
            the_tich = math.pi * a ** 2 * h
            title = f"Hình trụ với bán kính {a} và chiều cao {h}"

        elif selected_shape == "Hình nón":
            dien_tich_day = math.pi * a ** 2
            slant_height = math.sqrt(a ** 2 + h ** 2)
            dien_tich_xung_quanh = math.pi * a * slant_height
            dien_tich_toan_phan = dien_tich_xung_quanh + dien_tich_day
            the_tich = (1 / 3) * math.pi * a ** 2 * h
            title = f"Hình nón với bán kính {a} và chiều cao {h}"

        elif selected_shape == "Hình hộp":
            dien_tich_xung_quanh = 4 * a * h
            dien_tich_toan_phan = dien_tich_xung_quanh + 2 * a ** 2
            the_tich = a ** 2 * h
            title = f"Hình hộp với cạnh đáy {a} và chiều cao {h}"

        elif selected_shape == "Hình lục giác":
            dien_tich_day = (3 * math.sqrt(3) / 2) * a ** 2
            the_tich = dien_tich_day * h
            title = f"Hình lục giác đều với cạnh {a} và chiều cao {h}"

        else:
            raise ValueError("Chọn loại hình hợp lệ")

        # Vẽ hình lục giác trong không gian 3D (chỉ áp dụng cho hình lục giác)
        if selected_shape == "Hình lục giác":
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            theta = np.linspace(0, 2 * np.pi, 7)
            x_base = a * np.cos(theta)
            y_base = a * np.sin(theta)
            z_base = np.zeros_like(x_base)

            ax.plot(x_base, y_base, z_base, 'b-', lw=2)
            ax.plot(x_base, y_base, np.ones_like(z_base) * h, 'b-', lw=2)

            for i in range(len(x_base)):
                ax.plot([x_base[i], x_base[i]], [y_base[i], y_base[i]], [0, h], 'b-', lw=2)

            verts = [list(zip(x_base, y_base, z_base)),
                     list(zip(x_base, y_base, np.ones_like(z_base) * h))]
            ax.add_collection3d(Poly3DCollection(verts, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
            plt.title(title)
            plt.show()

        # Hiển thị kết quả tính toán
        messagebox.showinfo("Kết quả", f"Diện tích xung quanh: {dien_tich_xung_quanh:.2f}\n"
                                       f"Diện tích toàn phần: {dien_tich_toan_phan:.2f}\n"
                                       f"Thể tích: {the_tich:.2f}")

    except ValueError as e:
        messagebox.showerror("Lỗi", f"Giá trị không hợp lệ: {e}")

# Hàm thay đổi giao diện khi chọn hình học
def chon_hinh():
    selected_shape = combo.get()
    if selected_shape == "2D":
        frame_2d.pack(pady=10)
        frame_3d.pack_forget()
    else:
        frame_3d.pack(pady=10)
        frame_2d.pack_forget()


# Giao diện chính
root = tk.Tk()
root.title("Ứng dụng hỗ trợ học hình học")

# Khung lựa chọn hình học 2D hoặc 3D
frame = tk.Frame(root)
frame.pack(pady=10)

label_chon = tk.Label(frame, text="Chọn loại hình học:")
label_chon.grid(row=0, column=0, padx=10, pady=5)

combo = ttk.Combobox(frame, values=["2D", "3D"], state="readonly")
combo.grid(row=0, column=1, padx=10, pady=5)
combo.bind("<<ComboboxSelected>>", lambda e: chon_hinh())

# Khung 2D
frame_2d = tk.Frame(root)

label_2d = tk.Label(frame_2d, text="Chọn hình 2D:")
label_2d.grid(row=0, column=0, padx=10, pady=5)
combo_2d = ttk.Combobox(frame_2d, values=["Hình tròn", "Tam giác", "Tứ giác", "Hình thang"])
combo_2d.grid(row=0, column=1, padx=10, pady=5)

# Nhập bán kính cho hình tròn
label_ban_kinh = tk.Label(frame_2d, text="Nhập bán kính:")
label_ban_kinh.grid(row=1, column=0, padx=10, pady=5)
entry_ban_kinh = tk.Entry(frame_2d)
entry_ban_kinh.grid(row=1, column=1, padx=10, pady=5)

# Nhập các cạnh cho hình tam giác
label_canh_1 = tk.Label(frame_2d, text="Nhập cạnh 1:")
label_canh_1.grid(row=2, column=0, padx=10, pady=5)
entry_canh_1 = tk.Entry(frame_2d)
entry_canh_1.grid(row=2, column=1, padx=10, pady=5)

label_canh_2 = tk.Label(frame_2d, text="Nhập cạnh 2:")
label_canh_2.grid(row=3, column=0, padx=10, pady=5)
entry_canh_2 = tk.Entry(frame_2d)
entry_canh_2.grid(row=3, column=1, padx=10, pady=5)

label_canh_3 = tk.Label(frame_2d, text="Nhập cạnh 3:")
label_canh_3.grid(row=4, column=0, padx=10, pady=5)
entry_canh_3 = tk.Entry(frame_2d)
entry_canh_3.grid(row=4, column=1, padx=10, pady=5)

# Nhập chiều cao cho hình thang
label_canh_4 = tk.Label(frame_2d, text="Nhập cạnh 4 (cho tứ giác):")
label_canh_4.grid(row=5, column=0, padx=10, pady=5)
entry_canh_4 = tk.Entry(frame_2d)
entry_canh_4.grid(row=5, column=1, padx=10, pady=5)

# Nhập chiều cao cho hình thang
label_chieu_cao = tk.Label(frame_2d, text="Nhập chiều cao:")
label_chieu_cao.grid(row=6, column=0, padx=10, pady=5)
entry_chieu_cao = tk.Entry(frame_2d)
entry_chieu_cao.grid(row=6, column=1, padx=10, pady=5)

# Nút để tính toán cho hình 2D
button_tinh_2d = tk.Button(frame_2d, text="Tính 2D", command=tinh_hinh_2d)
button_tinh_2d.grid(row=7, column=0, pady=10)

# Nút để vẽ hình 2D
button_ve_2d = tk.Button(frame_2d, text="Vẽ 2D", command=ve_hinh_2d)
button_ve_2d.grid(row=7, column=1, pady=10)

# Khung 3D
frame_3d = tk.Frame(root)

label_3d = tk.Label(frame_3d, text="Hình 3D:")
label_3d.grid(row=0, column=0, padx=10, pady=5)
combo_3d = ttk.Combobox(frame_3d, values=["Hình trụ", "Hình cầu", "Hình nón", "Hình lục giác", "hinh hop"])
combo_3d.grid(row=0, column=1, padx=10, pady=5)

# Nhập cạnh cho hình lục giác và chiều cao cho các hình trụ, nón, lục giác
label_canh_luc_giac = tk.Label(frame_3d, text="Nhập bán kính hoặc cạnh đáy:")
label_canh_luc_giac.grid(row=1, column=0, padx=10, pady=5)
entry_canh_luc_giac = tk.Entry(frame_3d)
entry_canh_luc_giac.grid(row=1, column=1, padx=10, pady=5)

label_chieu_cao_3d = tk.Label(frame_3d, text="Nhập chiều cao:")
label_chieu_cao_3d.grid(row=2, column=0, padx=10, pady=5)
entry_chieu_cao = tk.Entry(frame_3d)
entry_chieu_cao.grid(row=2, column=1, padx=10, pady=5)

# Nút để vẽ hình 3D
button_ve_3d = tk.Button(frame_3d, text="Vẽ và Tính 3D", command=ve_hinh_3d())
button_ve_3d.grid(row=3, column=0, columnspan=2, pady=10)

# Hàm vẽ và tính toán cho hình 3D dựa trên lựa chọn

combo_3d = ttk.Combobox(frame_3d, values=["Hình trụ", "Hình nón", "Hình lục giác", "Hình hộp"])

# Chạy giao diện
root.mainloop()