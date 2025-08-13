import os
import subprocess
from pathlib import Path
import threading
from tkinter import Tk, Label, Button, filedialog, StringVar, messagebox
from concurrent.futures import ThreadPoolExecutor, as_completed

input_folder = Path()
output_folder = Path()
gs_path = None

# ===== TỰ ĐỘNG TÌM GHOSTSCRIPT =====
def find_ghostscript():
    possible_dirs = [
        r"C:\Program Files\gs",
        r"C:\Program Files (x86)\gs"
    ]
    for base_dir in possible_dirs:
        if Path(base_dir).exists():
            for folder in Path(base_dir).iterdir():
                exe_path = folder / "bin" / "gswin64c.exe"
                if exe_path.exists():
                    return str(exe_path)
                exe_path32 = folder / "bin" / "gswin32c.exe"
                if exe_path32.exists():
                    return str(exe_path32)
    return None

# ===== CHUYỂN PDF → PDF/A =====
def convert_to_pdfa(input_file, output_file):
    try:
        cmd = [
            gs_path,
            "-dPDFA=2",
            "-dBATCH",
            "-dNOPAUSE",
            "-dNOOUTERSAVE",
            "-sProcessColorModel=DeviceRGB",
            "-sDEVICE=pdfwrite",
            "-dFIXEDMEDIA",
            "-dPDFACompatibilityPolicy=2",
            f"-sOutputFile={str(output_file)}",
            str(input_file)
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW, text=True)
        if result.returncode != 0:
            return (input_file.name, False, result.stderr.strip())
        return (input_file.name, True, None)
    except Exception as e:
        return (input_file.name, False, str(e))

# ===== CHẠY CHUYỂN ĐỔI =====
def run_conversion():
    if not input_folder or not output_folder:
        messagebox.showerror("Lỗi", "Vui lòng chọn thư mục input và output!")
        return

    pdf_files = list(Path(input_folder).glob("*.pdf"))
    if not pdf_files:
        messagebox.showerror("Lỗi", "Không tìm thấy file PDF trong thư mục input!")
        return

    result_text.set(f"Đang xử lý {len(pdf_files)} file...")
    root.update()

    results = []
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(
                convert_to_pdfa,
                pdf_file,
                Path(output_folder) / pdf_file.name
            ): pdf_file
            for pdf_file in pdf_files
        }
        for future in as_completed(futures):
            results.append(future.result())

    success_count = sum(1 for _, ok, _ in results if ok)
    fail_count = len(results) - success_count

    # Tạo báo cáo lỗi
    if fail_count > 0:
        error_log = "\n".join([f"{name} → {err}" for name, ok, err in results if not ok])
        log_path = Path(output_folder) / "error_log.txt"
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(error_log)
        messagebox.showinfo("Hoàn tất", f"✅ Thành công: {success_count}\n❌ Lỗi: {fail_count}\nChi tiết lỗi lưu tại:\n{log_path}")
    else:
        messagebox.showinfo("Hoàn tất", f"✅ Thành công: {success_count}\n❌ Lỗi: {fail_count}")

    result_text.set("Xong!")

# ===== CHỌN THƯ MỤC =====
def choose_input():
    global input_folder
    folder = filedialog.askdirectory(title="Chọn thư mục chứa PDF")
    if folder:
        input_folder = Path(folder)
        input_text.set(f"Input: {folder}")

def choose_output():
    global output_folder
    folder = filedialog.askdirectory(title="Chọn thư mục lưu PDF/A")
    if folder:
        output_folder = Path(folder)
        output_text.set(f"Output: {folder}")

# ===== GUI =====
root = Tk()
root.title("PDF to PDF/A Converter (Ghostscript)")
root.geometry("500x220")

input_text = StringVar()
output_text = StringVar()
result_text = StringVar()

Label(root, textvariable=input_text).pack(pady=5)
Button(root, text="Chọn thư mục Input", command=choose_input).pack()

Label(root, textvariable=output_text).pack(pady=5)
Button(root, text="Chọn thư mục Output", command=choose_output).pack()

Button(root, text="Bắt đầu chuyển đổi", command=lambda: threading.Thread(target=run_conversion).start()).pack(pady=10)
Label(root, textvariable=result_text).pack()

# ===== KIỂM TRA GHOSTSCRIPT =====
gs_path = find_ghostscript()
if not gs_path:
    messagebox.showerror("Lỗi", "Không tìm thấy Ghostscript! Vui lòng cài đặt từ ghostscript.com")
    root.destroy()

root.mainloop()
