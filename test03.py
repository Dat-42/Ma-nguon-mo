import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, scrolledtext

# Đọc file CSV
df = pd.read_csv('diemPython.csv', index_col=0, header=0)
in_data = df.to_numpy()

# Lọc dữ liệu cho các lớp từ 1 đến 9
df_filtered = df[df.index.isin(range(1, 10))]
in_data_filtered = df_filtered.to_numpy()

# Hàm để hiển thị toàn bộ dữ liệu
def show_all_data():
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, df_filtered.to_string())

# Hàm để hiển thị thống kê điểm
def show_statistics():
    plt.figure()
    diemA_plus = in_data_filtered[:, 2]
    diemA = in_data_filtered[:, 3]
    diemB_plus = in_data_filtered[:, 4]
    diemB = in_data_filtered[:, 5]
    diemC_plus = in_data_filtered[:, 6]
    diemC = in_data_filtered[:, 7]
    diemD_plus = in_data_filtered[:, 8]
    diemD = in_data_filtered[:, 9]
    diemF = in_data_filtered[:, 10]


    plt.plot(range(len(diemA_plus)), diemA_plus, 'm-', label="Điểm A+")
    plt.plot(range(len(diemA)), diemA, 'r-', label="Điểm A")
    plt.plot(range(len(diemB_plus)), diemB_plus, 'g-', label="Điểm B+")
    plt.plot(range(len(diemB)), diemB, 'b-', label="Điểm B")
    plt.plot(range(len(diemC_plus)), diemC_plus, 'c-', label="Điểm C+")
    plt.plot(range(len(diemC)), diemC, 'y-', label="Điểm C")
    plt.plot(range(len(diemD_plus)), diemD_plus, 'orange', label="Điểm D+")
    plt.plot(range(len(diemD)), diemD, 'k-', label="Điểm D")
    plt.plot(range(len(diemF)), diemF, 'purple', label="Điểm F")
    plt.xlabel("Lớp")
    plt.ylabel("Số sinh viên đạt điểm")
    plt.legend(loc='upper right')
    plt.title("Thống kê điểm")
    plt.show()

# Hàm để hiển thị tổng số sinh viên đạt từng mức điểm
def show_total_by_grade():
    text_area.delete('1.0', tk.END)

    diemA_plus = in_data_filtered[:, 2]
    diemA = in_data_filtered[:, 3]
    diemB_plus = in_data_filtered[:, 4]
    diemB = in_data_filtered[:, 5]
    diemC_plus = in_data_filtered[:, 6]
    diemC = in_data_filtered[:, 7]
    diemD_plus = in_data_filtered[:, 8]
    diemD = in_data_filtered[:, 9]
    diemF = in_data_filtered[:, 10]

    total_a_plus = np.sum(diemA_plus)
    total_a = np.sum(diemA)
    total_b_plus = np.sum(diemB_plus)
    total_b = np.sum(diemB)
    total_c_plus = np.sum(diemC_plus)
    total_c = np.sum(diemC)
    total_d_plus = np.sum(diemD_plus)
    total_d = np.sum(diemD)
    total_f = np.sum(diemF)

    # Hiển thị tổng số sinh viên đạt từng điểm
    text_area.insert(tk.END, f"Tổng số sinh viên đạt điểm A+: {total_a_plus}\n")
    text_area.insert(tk.END, f"Tổng số sinh viên đạt điểm A: {total_a}\n")
    text_area.insert(tk.END, f"Tổng số sinh viên đạt điểm B+: {total_b_plus}\n")
    text_area.insert(tk.END, f"Tổng số sinh viên đạt điểm B: {total_b}\n")
    text_area.insert(tk.END, f"Tổng số sinh viên đạt điểm C+: {total_c_plus}\n")
    text_area.insert(tk.END, f"Tổng số sinh viên đạt điểm C: {total_c}\n")
    text_area.insert(tk.END, f"Tổng số sinh viên đạt điểm D+: {total_d_plus}\n")
    text_area.insert(tk.END, f"Tổng số sinh viên đạt điểm D: {total_d}\n")
    text_area.insert(tk.END, f"Tổng số sinh viên đạt điểm F: {total_f}\n")


# Tạo cửa sổ chính
root = tk.Tk()
root.title("Quản lý điểm")
root.geometry("1500x500")  # Đặt kích thước cửa sổ lớn hơn

# Tạo khung cho các nút
frame_buttons = ttk.Frame(root)
frame_buttons.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Tạo khung cho khu vực hiển thị văn bản
frame_text = ttk.Frame(root)
frame_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Tạo các nút lựa chọn
btn_all_data = ttk.Button(frame_buttons, text="Hiển thị toàn bộ dữ liệu", command=show_all_data)
btn_statistics = ttk.Button(frame_buttons, text="Biểu đồ điểm thi", command=show_statistics)
btn_total_by_grade = ttk.Button(frame_buttons, text="Tổng sinh viên theo điểm", command=show_total_by_grade)

# Đặt các nút lên khung
btn_all_data.pack(pady=5)
btn_statistics.pack(pady=5)
btn_total_by_grade.pack(pady=5)


# Tạo khu vực hiển thị văn bản
text_area = scrolledtext.ScrolledText(frame_text, width=100, height=80)  # Đặt kích thước khu vực văn bản lớn hơn
text_area.pack(fill=tk.BOTH, expand=True)

# Chạy ứng dụng
root.mainloop()
