try:
    import cv2
    print("✓ OpenCV импортирован")
    print(f"Версия: {cv2.__version__}")
except ImportError:
    print("ОШИБКА: OpenCV не установлен!")
    print("Установите: pip install opencv-contrib-python")
    exit()

import os
from pathlib import Path
import time

# Создание папки для результатов
output_folder = "experiment_videos"
os.makedirs(output_folder, exist_ok=True)

# ПАРАМЕТРЫ ЗАПИСИ (НЕ МЕНЯТЬ!)
DURATION_SEC = 8
FPS = 25  # Фиксированный FPS
TOTAL_FRAMES = FPS * DURATION_SEC  # = 200 кадров

print("="*70)
print("ЗАПИСЬ ВИДЕО С КАМЕРЫ")
print("="*70)
print(f"\nПараметры:")
print(f"  FPS: {FPS}")
print(f"  Длительность: {DURATION_SEC} секунд")
print(f"  Всего кадров: {TOTAL_FRAMES}")

# Подключение к камере
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("\n❌ ОШИБКА: Не удалось подключиться к камере!")
    print("Проверьте:")
    print("  - Камера подключена")
    print("  - Iriun Webcam запущен (если используете телефон)")
    print("  - Камера не занята другим приложением")
    exit()

# Установка разрешения
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

# Получение фактического разрешения
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"  Разрешение: {width}x{height}")

# Форматы видео
video_formats = {
    'MP4': {
        'ext': 'mp4',
        'codecs': ['mp4v', 'MP4V', 'avc1']
    },
    'DivX': {
        'ext': 'avi',
        'codecs': ['DIVX', 'divx']
    },
    'FLV': {
        'ext': 'flv',
        'codecs': ['FLV1', 'flv']
    },
    'XVID': {
        'ext': 'avi',
        'codecs': ['XVID', 'xvid']
    }
}

writers = {}
print("\n" + "-"*70)
print("Инициализация кодеков...")
print("-"*70)

for format_name, format_info in video_formats.items():
    writer_created = False
    
    for codec in format_info['codecs']:
        try:
            fourcc = cv2.VideoWriter.fourcc(*codec)
            filename = f"{output_folder}/Video_{format_name}.{format_info['ext']}"
            
            # ВАЖНО: Явно указываем FPS = 25
            writer = cv2.VideoWriter(filename, fourcc, FPS, (width, height))
            
            if writer.isOpened():
                writers[format_name] = {
                    'writer': writer,
                    'filename': filename
                }
                print(f"✓ {format_name:<10} - кодек: {codec:<6} FPS: {FPS}")
                writer_created = True
                break
        except Exception as e:
            continue
    
    if not writer_created:
        print(f"✗ {format_name:<10} - не удалось создать")

if not writers:
    print("\n❌ ОШИБКА: Не удалось создать ни один видео-писатель!")
    cap.release()
    exit()

print("\n" + "="*70)
print("НАЧАЛО ЗАПИСИ")
print("="*70)
print("Смотрите в камеру! Запись начнётся через 3 секунды...")

# Обратный отсчёт
for i in range(3, 0, -1):
    print(f"{i}...")
    time.sleep(1)

print("🔴 ЗАПИСЬ!")

# Запись кадров
frame_count = 0
start_time = time.time()

while frame_count < TOTAL_FRAMES:
    ret, frame = cap.read()
    
    if not ret:
        print(f"\n❌ Ошибка захвата кадра #{frame_count + 1}")
        break
    
    # Запись во все форматы
    for format_name, writer_info in writers.items():
        writer_info['writer'].write(frame)
    
    frame_count += 1
    
    # Прогресс каждые 50 кадров
    if frame_count % 50 == 0:
        elapsed = time.time() - start_time
        print(f"Записано: {frame_count}/{TOTAL_FRAMES} кадров ({round(elapsed, 1)} сек)")

# Завершение
end_time = time.time()
total_time = end_time - start_time

print(f"\n✓ ЗАПИСЬ ЗАВЕРШЕНА!")
print(f"Записано кадров: {frame_count}/{TOTAL_FRAMES}")
print(f"Время записи: {round(total_time, 2)} сек")
print(f"Фактический FPS: {round(frame_count / total_time, 2)}")

# Освобождение ресурсов
for writer_info in writers.values():
    writer_info['writer'].release()
cap.release()
cv2.destroyAllWindows()

# Проверка созданных файлов
print("\n" + "="*70)
print("СОЗДАННЫЕ ФАЙЛЫ:")
print("="*70)

for format_name, writer_info in writers.items():
    filename = writer_info['filename']
    if os.path.exists(filename):
        file_size = Path(filename).stat().st_size
        size_mb = round(file_size / 1e6, 3)
        
        # Проверяем FPS в созданном файле
        test_cap = cv2.VideoCapture(filename)
        if test_cap.isOpened():
            saved_fps = test_cap.get(cv2.CAP_PROP_FPS)
            saved_frames = int(test_cap.get(cv2.CAP_PROP_FRAME_COUNT))
            test_cap.release()
            
            print(f"{format_name:<10} {size_mb:>8} MB | FPS: {saved_fps} | Кадров: {saved_frames}")
        else:
            print(f"{format_name:<10} {size_mb:>8} MB | ⚠ Не удалось проверить")
    else:
        print(f"{format_name:<10} {'не создан':>10}")

print("\n" + "="*70)
print(f"Все видео сохранены в папке '{output_folder}'")
print("="*70)