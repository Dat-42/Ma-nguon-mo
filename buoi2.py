import numpy as np
import tkinter as tk
from tkinter import messagebox
import os

def load_data(file_path):
    """Load data from a CSV file into a numpy array."""
    try:
        data = np.genfromtxt(file_path, delimiter=',', dtype=str, encoding='utf-8', skip_header=1)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return np.array([])


def search_student(data, student_id=None, student_name=None):
    """Search for a student's information by ID or Name."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    if student_id:  # Tìm kiếm theo ID
        student_data = data[data[:, 0] == student_id]
        if student_data.size == 0:
            return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    elif student_name:  # Tìm kiếm theo tên
        student_data = data[data[:, 1] == student_name]
        if student_data.size == 0:
            return f"Không tìm thấy thông tin cho sinh viên có tên {student_name}."
    else:
        return "Vui lòng nhập ID hoặc tên sinh viên để tìm kiếm."

    return "\n".join([", ".join(row) for row in student_data])
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)


def search_subject(data, subject_name):
    """Search for grades of a specific subject."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    subject_data = data[data[:, 2] == subject_name]
    if subject_data.size == 0:
        return f"Không tìm thấy điểm cho môn học {subject_name}."
    else:
        return "\n".join([f"ID: {row[0]}, Tên: {row[1]}, Điểm: {row[3]}" for row in subject_data])

def calculate_average(data, student_id):
    """Calculate the average grade for a specific student using numpy."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    else:
        try:
            grades = student_data[:, 3].astype(float)  # Convert grades to float
            average_grade = np.mean(grades)
            return f"Trung bình cộng điểm của sinh viên có ID {student_id} là {average_grade:.2f}."
        except ValueError:
            return "Có lỗi khi chuyển đổi điểm sang số thực. Vui lòng kiểm tra dữ liệu."

def search_action():
    choice = choice_var.get()
    student_id = id_entry.get().strip()
    student_name = name_entry.get().strip()
    subject_name = subject_entry.get().strip()

    if choice == '1':  # Tìm kiếm thông tin sinh viên
        if student_id:
            result = search_student(data, student_id=student_id)
        elif student_name:
            result = search_student(data, student_name=student_name)
        else:
            result = "Vui lòng nhập ID hoặc tên sinh viên để tìm kiếm."
    elif choice == '2':  # Tìm kiếm điểm môn học
        result = search_subject(data, subject_name)
    elif choice == '3':  # Tính TBC điểm của sinh viên
        result = calculate_average(data, student_id)  # Tính TBC chỉ qua ID
    else:
        result = "Lựa chọn không hợp lệ."

    messagebox.showinfo("Kết quả", result)
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)


def add_students():
    idsv = id_entry.get().strip()
    name = name_entry.get().strip()
    subject = subject_entry.get().strip()
    score = score_entry.get().strip()

    if not idsv or not name or not subject or not score:
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
        return

    try:
        # Kiểm tra xem điểm có phải là số hợp lệ hay không
        score_float = float(score)
    except ValueError:
        messagebox.showwarning("Cảnh báo", "Điểm phải là một số hợp lệ!")
        return

    try:
        with open(file_path, 'a', encoding="utf-8") as file:
            file.write(f"{idsv},{name},{subject},{score_float}\n")
        messagebox.showinfo("Thông báo", "Thêm sinh viên thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm sinh viên: {e}")

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    score_entry.delete(0, tk.END)


def show_students():

    if data.size == 0:
        messagebox.showinfo("Danh sách sinh viên", "Không có dữ liệu sinh viên.")
        return

    student_list = "\n".join([", ".join(row) for row in data])

    # Hiển thị danh sách sinh viên trong một messagebox
    messagebox.showinfo("Danh sách sinh viên", student_list)
def delete_student():
    """Xóa sinh viên dựa trên ID."""
    student_id = id_entry.get().strip()  # Lấy ID sinh viên từ input

    if not student_id:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID sinh viên để xóa!")
        return

    global data
    # Tìm sinh viên theo ID
    student_data = data[data[:, 0] == student_id]

    if student_data.size == 0:
        messagebox.showwarning("Cảnh báo", f"Không tìm thấy sinh viên có ID {student_id}.")
        return

    # Xóa sinh viên khỏi data
    data = data[data[:, 0] != student_id]

    # Ghi dữ liệu mới vào file CSV
    try:
        # Mở file để ghi lại dữ liệu sau khi xóa
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write("ID,Name,Subject,Score\n")  # Ghi lại tiêu đề
            for row in data:
                file.write(",".join(row) + "\n")  # Ghi từng sinh viên vào file
        messagebox.showinfo("Thông báo", f"Đã xóa sinh viên có ID {student_id} thành công!")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xóa sinh viên: {e}")

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    score_entry.delete(0, tk.END)

def main():
    global data, file_path
    file_path = 'data.csv'  # Đặt đường dẫn đến file dữ liệu của bạn
    data = load_data(file_path)

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Tìm kiếm thông tin sinh viên")

    # Đặt kích thước cửa sổ 600x900
    root.geometry("600x650")

    # Đảm bảo các widget được căn giữa
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    container = tk.Frame(root)
    container.place(relx=0.5, rely=0.5, anchor="center")  # Căn giữa frame chứa các widget

    # Thêm các widget
    tk.Label(root, text="Chọn hành động:").pack(pady=5)

    global choice_var
    choice_var = tk.StringVar(value='1')

    tk.Radiobutton(root, text="Tìm kiếm thông tin sinh viên", variable=choice_var, value='1').pack(anchor='center')
    tk.Radiobutton(root, text="Tìm kiếm điểm môn học", variable=choice_var, value='2').pack(anchor='center')
    tk.Radiobutton(root, text="Tính TBC điểm của sinh viên", variable=choice_var, value='3').pack(anchor='center')

    tk.Label(root, text="ID sinh viên:").pack(pady=5)
    global id_entry
    id_entry = tk.Entry(root)
    id_entry.pack(pady=5)

    tk.Label(root, text="Tên môn học (nếu có):").pack(pady=5)
    global subject_entry
    subject_entry = tk.Entry(root)
    subject_entry.pack(pady=5)

    tk.Label(root, text="Tên sinh viên:").pack(pady=5)
    global name_entry
    name_entry = tk.Entry(root)
    name_entry.pack(pady=5)

    tk.Label(root, text="Điểm:").pack(pady=5)
    global score_entry
    score_entry = tk.Entry(root)
    score_entry.pack(pady=5)

    tk.Button(root, text="Tìm kiếm", command=search_action).pack(pady=10)
    tk.Button(root, text="Thêm sinh viên", command=add_students).pack(pady=10)
    tk.Button(root, text="Show danh sách", command=show_students).pack(pady=10)
    tk.Button(root, text="Xóa sinh viên", command=delete_student).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
