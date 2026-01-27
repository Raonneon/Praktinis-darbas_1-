try:
    import cv2
    print("✓ OpenCV успешно импортирован")
    print(f"Версия: {cv2.__version__}")
except ImportError as e:
    print("ОШИБКА: OpenCV не установлен!")
    print("\nУстановите OpenCV командой:")
    print("  pip install opencv-contrib-python")
    exit()

import os
from pathlib import Path

# Создание папки для результатов
output_folder = "experiment_videos"
os.makedirs(output_folder, exist_ok=True)

# ВАЖНО: Укажите путь к вашему исходному изображению
SOURCE_IMAGE = "your_photo.jpg"  # Замените на имя вашего файла!

# Параметры записи
DURATION_SEC = 8  # Длительность в секундах
FPS = 25          # Кадров в секунду
TOTAL_FRAMES = FPS * DURATION_SEC  # 200 кадров (25 * 8)

# Если видео получается слишком коротким, увеличьте эти значения:
# DURATION_SEC = 10  # для 250 кадров при FPS=25
# DURATION_SEC = 20  # для 500 кадров при FPS=25

print("\n" + "="*70)
print("СОЗДАНИЕ ВИДЕО ИЗ СТАТИЧНОГО ИЗОБРАЖЕНИЯ")
print("="*70)

# Проверка существования файла
if not os.path.exists(SOURCE_IMAGE):
    print(f"\nОШИБКА: Файл '{SOURCE_IMAGE}' не найден!")
    print("Поместите ваше фото в папку со скриптом и укажите правильное имя")
    exit()

# Загрузка изображения
frame = cv2.imread(SOURCE_IMAGE)

if frame is None:
    print(f"\nОШИБКА: Не удалось загрузить изображение '{SOURCE_IMAGE}'")
    exit()

# Получение размеров изображения
height, width = frame.shape[:2]

print(f"\nИсходное изображение: {SOURCE_IMAGE}")
print(f"Разрешение: {width}x{height}")
print(f"FPS: {FPS}")
print(f"Длительность: {DURATION_SEC} сек")
print(f"Всего кадров: {TOTAL_FRAMES}")

# Форматы видео с альтернативными кодеками
video_formats = {
    'MP4': {
        'ext': 'mp4',
        'codecs': ['mp4v', 'MP4V', 'avc1', 'H264']
    },
    'AVI_XVID': {
        'ext': 'avi',
        'codecs': ['XVID', 'xvid', 'X264']
    },
    'AVI_MJPEG': {
        'ext': 'avi',
        'codecs': ['MJPG', 'MJPEG']
    },
    'AVI_DIVX': {
        'ext': 'avi',
        'codecs': ['DIVX', 'divx']
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
            writer = cv2.VideoWriter(filename, fourcc, FPS, (width, height))
            
            if writer.isOpened():
                writers[format_name] = writer
                print(f"✓ {format_name:<15} - кодек: {codec}")
                writer_created = True
                break
        except Exception as e:
            continue
    
    if not writer_created:
        print(f"✗ {format_name:<15} - не удалось создать (пропускаем)")

if not writers:
    print("\nОШИБКА: Не удалось создать ни один видео-писатель!")
    print("Проверьте установку OpenCV или попробуйте переустановить:")
    print("  pip uninstall opencv-python opencv-contrib-python")
    print("  pip install opencv-contrib-python")
    exit()

print("\n" + "-"*70)
print("Создание видео файлов...")
print("-"*70)

# Запись кадров
for frame_count in range(TOTAL_FRAMES):
    for format_name, writer in writers.items():
        writer.write(frame)
    
    if (frame_count + 1) % 50 == 0:
        print(f"Записано кадров: {frame_count + 1}/{TOTAL_FRAMES}")

# Освобождение ресурсов
for writer in writers.values():
    writer.release()

print(f"\n✓ Создание видео завершено! Записано {TOTAL_FRAMES} кадров")

# Вывод размеров файлов
print("\n" + "="*70)
print("РАЗМЕРЫ ВИДЕО ФАЙЛОВ:")
print("="*70)

for format_name, format_info in video_formats.items():
    filename = f"{output_folder}/Video_{format_name}.{format_info['ext']}"
    if os.path.exists(filename):
        file_size = Path(filename).stat().st_size
        size_mb = round(file_size / 1e6, 3)
        print(f"{format_name:<15} {size_mb:>10} MB")
    else:
        print(f"{format_name:<15} {'не создан':>10}")

print("\n" + "="*70)
print(f"Все видео сохранены в папке '{output_folder}'")
print("="*70)