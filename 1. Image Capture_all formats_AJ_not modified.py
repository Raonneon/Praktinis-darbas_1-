import cv2
import os
from pathlib import Path

# Создание папки для результатов
output_folder = "experiment_images"
os.makedirs(output_folder, exist_ok=True)

# Номер эксперимента (измените для каждого эксперимента: 1, 2, 3, 4, 5)
EXPERIMENT_NUM = 1

# Подключение к камере
cap = cv2.VideoCapture(0)

# Автоматическое определение максимальной доступной резолюции
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

# Получение фактической резолюции
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Эксперимент #{EXPERIMENT_NUM}")
print(f"Резолюция камеры: {width}x{height}")

# Захват одного кадра
ret, frame = cap.read()

if ret:
    # Форматы для сохранения
    formats = {
        'BMP': '.bmp',
        'JPG': '.jpg',
        'PNG': '.png',
        'TIF': '.tif'
    }
    
    print("\nСоздание цветных изображений:")
    for format_name, extension in formats.items():
        filename = f"{output_folder}/Exp{EXPERIMENT_NUM}_{format_name}_Color{extension}"
        cv2.imwrite(filename, frame)
        
        # Получение размера файла
        file_size = Path(filename).stat().st_size
        print(f"{format_name}: {round(file_size / 1e6, 3)} MB")
    
    # Конвертация в Grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    print("\nСоздание черно-белых изображений:")
    for format_name, extension in formats.items():
        filename = f"{output_folder}/Exp{EXPERIMENT_NUM}_{format_name}_Gray{extension}"
        cv2.imwrite(filename, gray_frame)
        
        # Получение размера файла
        file_size = Path(filename).stat().st_size
        print(f"{format_name} (B/W): {round(file_size / 1e6, 3)} MB")
    
    print(f"\n✓ Эксперимент #{EXPERIMENT_NUM} завершен успешно!")
    print(f"Все файлы сохранены в папке '{output_folder}'")
    
else:
    print("Ошибка: не удалось захватить изображение с камеры")

# Освобождение камеры
cap.release()
cv2.destroyAllWindows()