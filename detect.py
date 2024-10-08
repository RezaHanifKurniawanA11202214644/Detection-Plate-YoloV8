import os
from ultralytics import YOLO

# Muat model yang sudah dilatih
model = YOLO('../Detection-plat/runs/detect/train/weights/best.pt')

# Tentukan direktori yang berisi gambar uji
test_images_dir = '../Detection-plat/test/'  # Ganti ini dengan path ke folder yang berisi gambar uji

# Dapatkan daftar gambar dengan ekstensi yang valid
valid_extensions = ('.jpg', '.png', '.jpeg')
test_images = [f for f in os.listdir(test_images_dir) if f.endswith(valid_extensions)]

# Periksa apakah ada gambar yang akan diproses
if not test_images:
    print("Tidak ada gambar yang ditemukan di direktori uji.")
else:
    # Buat direktori 'results' jika belum ada
    results_dir = '../Detection-plat/results'
    os.makedirs(results_dir, exist_ok=True)
    
    # Proses setiap gambar dalam folder
    for image_name in test_images:
        image_path = os.path.join(test_images_dir, image_name)
        results = model(image_path)  # Lakukan deteksi
        
        # Periksa apakah ada deteksi
        if results:
            # Simpan gambar hasil deteksi di direktori 'results'
            for result in results:
                save_path = os.path.join(results_dir, image_name)
                result.save(save_path)  # Simpan hasil di path yang ditentukan
            print(f"Hasil deteksi untuk {image_name} disimpan di {results_dir}")
        else:
            print(f"Tidak ada deteksi untuk {image_name}")