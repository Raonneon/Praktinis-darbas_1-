from PIL import Image
import os
from pathlib import Path

def get_image_info(image_path):
    """Получает информацию об изображении"""
    if not os.path.exists(image_path):
        return None
    
    try:
        img = Image.open(image_path)
        width, height = img.size
        file_size = Path(image_path).stat().st_size
        
        # Определение количества каналов
        if img.mode == 'RGB':
            channels = 3
        elif img.mode == 'L':
            channels = 1
        elif img.mode == 'RGBA':
            channels = 4
        else:
            channels = len(img.getbands())
        
        return {
            'size_mb': round(file_size / 1e6, 3),
            'resolution': f"{width}x{height}",
            'channels': channels,
            'mode': img.mode
        }
    except Exception as e:
        print(f"Ошибка чтения {image_path}: {e}")
        return None

# ===== АНАЛИЗ ЭКСПЕРИМЕНТАЛЬНЫХ ИЗОБРАЖЕНИЙ =====
print("="*90)
print("РЕЗУЛЬТАТЫ ЭКСПЕРИМЕНТОВ С ИЗОБРАЖЕНИЯМИ")
print("="*90)

experiment_folder = "experiment_images"
formats = ['BMP', 'JPG', 'PNG', 'TIF']
types = ['Color', 'Gray']

if os.path.exists(experiment_folder):
    # Определяем количество экспериментов
    files = os.listdir(experiment_folder)
    exp_nums_set = set()
    
    for f in files:
        if f.startswith('Exp') and '_' in f:
            try:
                exp_num = int(f.split('_')[0].replace('Exp', ''))
                exp_nums_set.add(exp_num)
            except ValueError:
                continue
    
    exp_numbers = sorted(exp_nums_set)
    
    if exp_numbers:
        for exp_num in exp_numbers:
            print(f"\n{'='*90}")
            print(f"ЭКСПЕРИМЕНТ #{exp_num}")
            print(f"{'='*90}")
            print(f"{'Формат':<10} {'Тип':<10} {'Размер (MB)':<15} {'Разрешение':<15} {'Режим':<10} {'Каналы':<10}")
            print("-" * 90)
            
            for fmt in formats:
                for typ in types:
                    filename = f"Exp{exp_num}_{fmt}_{typ}"
                    
                    # Определяем расширение
                    ext_map = {
                        'BMP': '.bmp',
                        'JPG': '.jpg',
                        'PNG': '.png',
                        'TIF': '.tif'
                    }
                    
                    ext = ext_map.get(fmt, '.jpg')
                    filepath = os.path.join(experiment_folder, filename + ext)
                    
                    info = get_image_info(filepath)
                    if info:
                        print(f"{fmt:<10} {typ:<10} {info['size_mb']:<15} {info['resolution']:<15} {info['mode']:<10} {info['channels']:<10}")
                    else:
                        print(f"{fmt:<10} {typ:<10} {'Файл не найден':<15}")
        
        # ===== СТАТИСТИКА ПО ФОРМАТАМ =====
        print("\n" + "="*90)
        print("СРЕДНИЕ ЗНАЧЕНИЯ ПО ФОРМАТАМ")
        print("="*90)
        
        for typ in types:
            print(f"\n--- {typ} изображения ---")
            print(f"{'Формат':<10} {'Средний размер (MB)':<25} {'Min (MB)':<15} {'Max (MB)':<15}")
            print("-" * 70)
            
            for fmt in formats:
                sizes = []
                ext_map = {
                    'BMP': '.bmp',
                    'JPG': '.jpg',
                    'PNG': '.png',
                    'TIF': '.tif'
                }
                
                for exp_num in exp_numbers:
                    filename = f"Exp{exp_num}_{fmt}_{typ}"
                    ext = ext_map.get(fmt, '.jpg')
                    filepath = os.path.join(experiment_folder, filename + ext)
                    
                    info = get_image_info(filepath)
                    if info:
                        sizes.append(info['size_mb'])
                
                if sizes:
                    avg = round(sum(sizes) / len(sizes), 3)
                    min_size = round(min(sizes), 3)
                    max_size = round(max(sizes), 3)
                    print(f"{fmt:<10} {avg:<25} {min_size:<15} {max_size:<15}")
                else:
                    print(f"{fmt:<10} {'Нет данных':<25}")
    else:
        print("\nЭкспериментальные файлы не найдены")
else:
    print(f"\nПапка '{experiment_folder}' не найдена")

print("\n" + "="*90)
print("✓ Анализ завершен")
print("="*90)