import os
from tkinter import Tk, filedialog
from PIL import Image
import fitz  # PyMuPDF

def compress_image(input_path, output_path, quality=85, max_size_kb=1024):
    """Compress the image until it's under the target size (in KB)."""
    img = Image.open(input_path).convert("RGB")
    q = quality
    while q > 10:
        img.save(output_path, "JPEG", quality=q, optimize=True)
        if os.path.getsize(output_path) / 1024 <= max_size_kb:
            break
        q -= 5
    return output_path

def convert_jpg_to_pdf():
    root = Tk()
    root.withdraw()  # Hide the main tkinter window

    # 📂 Ask user to select a JPG image
    input_path = filedialog.askopenfilename(
        title="Select a JPG file",
        filetypes=[("JPEG Files", "*.jpg;*.jpeg")]
    )
    if not input_path:
        print("❌ No file selected.")
        return

    # 📍 Suggest default output path with same name but .pdf
    default_output = os.path.splitext(input_path)[0] + ".pdf"

    # 💾 Ask user where to save the PDF
    output_path = filedialog.asksaveasfilename(
        title="Save PDF As",
        defaultextension=".pdf",
        initialfile=os.path.basename(default_output),
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not output_path:
        print("❌ No save location selected.")
        return

    # 🛠️ Compress + Convert
    temp_jpg = "temp_compressed.jpg"
    compress_image(input_path, temp_jpg)

    # Convert using PyMuPDF
    doc = fitz.open()
    img = fitz.open(temp_jpg)
    img_pdf = fitz.open("pdf", img.convert_to_pdf())
    doc.insert_pdf(img_pdf)
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    os.remove(temp_jpg)

    print(f"✅ PDF saved as: {output_path} ({os.path.getsize(output_path) / 1024:.2f} KB)")

# 🏁 Run the converter
if __name__ == "__main__":
    convert_jpg_to_pdf()
