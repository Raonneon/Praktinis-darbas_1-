import cv2
import os
from pathlib import Path

video_folder = "experiment_videos"

print("="*80)
print("ДИАГНОСТИКА ВИДЕО ФАЙЛОВ")
print("="*80)

if not os.path.exists(video_folder):
    print(f"\nПапка '{video_folder}' не найдена!")
    exit()

video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.flv'))]

if not video_files:
    print(f"\nВ папке '{video_folder}' нет видео файлов!")
    exit()

for video_file in sorted(video_files):
    video_path = os.path.join(video_folder, video_file)
    
    print(f"\n{'='*80}")
    print(f"Файл: {video_file}")
    print(f"{'='*80}")
    
    # Размер файла
    file_size = Path(video_path).stat().st_size
    print(f"Размер файла: {round(file_size / 1e6, 3)} MB")
    
    # Открываем видео
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("❌ ОШИБКА: Не удалось открыть видео файл")
        print("   Возможные причины:")
        print("   - Отсутствует необходимый кодек")
        print("   - Файл повреждён")
        print("   - Неподдерживаемый формат")
        continue
    
    # Получаем свойства видео
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    
    # Декодируем FOURCC
    fourcc_str = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
    
    duration = total_frames / fps if fps > 0 else 0
    
    print(f"\n📊 ПАРАМЕТРЫ ВИДЕО:")
    print(f"   Разрешение: {width}x{height}")
    print(f"   FPS: {fps}")
    print(f"   Кадров: {total_frames}")
    print(f"   Длительность: {round(duration, 2)} сек")
    print(f"   Кодек (FOURCC): {fourcc_str}")
    
    # Проверяем возможность чтения кадров
    print(f"\n🔍 ТЕСТ ЧТЕНИЯ КАДРОВ:")
    
    # Пробуем прочитать первый кадр
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ret, frame = cap.read()
    if ret:
        print(f"   ✓ Первый кадр: OK")
    else:
        print(f"   ✗ Первый кадр: ОШИБКА")
    
    # Пробуем прочитать 100-й кадр
    if total_frames >= 100:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 99)
        ret, frame = cap.read()
        if ret:
            print(f"   ✓ 100-й кадр: OK")
        else:
            print(f"   ✗ 100-й кадр: ОШИБКА")
    else:
        print(f"   ⚠ 100-й кадр: Недостаточно кадров (всего {total_frames})")
    
    # Пробуем прочитать последний кадр
    if total_frames > 0:
        cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
        ret, frame = cap.read()
        if ret:
            print(f"   ✓ Последний кадр: OK")
        else:
            print(f"   ✗ Последний кадр: ОШИБКА")
    
    cap.release()

print("\n" + "="*80)
print("✓ Диагностика завершена")
print("="*80)