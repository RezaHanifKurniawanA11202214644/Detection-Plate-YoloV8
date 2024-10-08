import os
from PIL import Image  # Menggunakan Pillow untuk mendapatkan dimensi gambar

def convert_to_yolo_format(xmin, ymin, width, height, img_width, img_height):
    # Hitung xmax dan ymax
    xmax = xmin + width
    ymax = ymin + height

    # Hitung center
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2

    # Normalisasi
    x_center_normalized = x_center / img_width
    y_center_normalized = y_center / img_height
    width_normalized = width / img_width
    height_normalized = height / img_height

    # Class ID (Misalnya 0 untuk plat nomor)
    class_id = 0

    return class_id, x_center_normalized, y_center_normalized, width_normalized, height_normalized

def create_yolo_label_file(image_name, xmin, ymin, width, height, label_dir, image_dir):
    # Baca gambar untuk mendapatkan dimensi
    image_path = os.path.join(image_dir, image_name)
    with Image.open(image_path) as img:
        img_width, img_height = img.size

    # Konversi ke format YOLO
    class_id, x_center, y_center, width_normalized, height_normalized = convert_to_yolo_format(
        xmin, ymin, width, height, img_width, img_height
    )

    # Buat file label
    txt_name = os.path.splitext(image_name)[0] + '.txt'
    txt_path = os.path.join(label_dir, txt_name)
    with open(txt_path, 'w') as f:
        f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width_normalized:.6f} {height_normalized:.6f}\n")

def process_individual_txt_files(txt_dir, label_dir, image_dir):
    # Daftar semua file teks dalam direktori
    txt_files = [f for f in os.listdir(txt_dir) if f.endswith('.txt')]

    for txt_file in txt_files:
        txt_path = os.path.join(txt_dir, txt_file)
        image_name = os.path.splitext(txt_file)[0]
        if os.path.exists(os.path.join(image_dir, image_name + '.jpg')):
            image_name += '.jpg'
        elif os.path.exists(os.path.join(image_dir, image_name + '.png')):
            image_name += '.png'
        elif os.path.exists(os.path.join(image_dir, image_name + '.jpeg')):
            image_name += '.jpeg'

        # Baca file teks untuk mendapatkan bounding box
        with open(txt_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split()

            # Pastikan setidaknya ada 5 elemen, abaikan elemen nama gambar
            if len(parts) < 5:
                print(f"Data format error in file {txt_file}, line: {line}")
                continue
            
            # Ambil 4 elemen terakhir sebagai xmin, ymin, width, height
            try:
                xmin = int(parts[-5])  # xmin
                ymin = int(parts[-4])  # ymin
                width = int(parts[-3])  # width
                height = int(parts[-2])  # height
                plate_number = parts[-1]  # Plat nomor (tidak digunakan dalam YOLO format)
            except ValueError:
                print(f"Skipping line due to invalid format: {line}")
                continue

            # Buat file label YOLO
            create_yolo_label_file(image_name, xmin, ymin, width, height, label_dir, image_dir)

# Contoh penggunaan
train_txt_dir = '../Detection-plat/assets/train'  # Path folder file teks train
val_txt_dir = '../Detection-plat/assets/val'  # Path folder file teks val

label_train_dir = '../Detection-plat/datasets/labels/train'  # Path folder untuk label YOLO train
label_val_dir = '../Detection-plat/datasets/labels/val'  # Path folder untuk label YOLO val

image_train_dir = '../Detection-plat/datasets/images/train'  # Path folder gambar train
image_val_dir = '../Detection-plat/datasets/images/val'  # Path folder gambar val

os.makedirs(label_train_dir, exist_ok=True)
os.makedirs(label_val_dir, exist_ok=True)

# Proses file teks untuk train dan val
process_individual_txt_files(train_txt_dir, label_train_dir, image_train_dir)
process_individual_txt_files(val_txt_dir, label_val_dir, image_val_dir)
