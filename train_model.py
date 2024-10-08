from ultralytics import YOLO

# Muat model YOLOv8
model = YOLO('yolov8n.yaml')  # Model YOLOv8 Nano (versi lebih ringan)

# Melatih model pada dataset plat nomor
model.train(data='D:/SMTR 5/Komputer Vision/Tugas/Detection-plat/dataset.yaml', epochs=100, imgsz=640)
