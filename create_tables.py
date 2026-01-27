try:
    from PIL import Image
except ImportError:
    print("Установите Pillow: pip install Pillow")
    exit()

import os
from pathlib import Path

# Папки с результатами
experiment_folder = "experiment_images"
video_folder = "experiment_videos"

print("="*80)
print("СОЗДАНИЕ ТАБЛИЦ РЕЗУЛЬТАТОВ")
print("="*80)

# ============================================================================
# 1. ТАБЛИЦА РЕЗУЛЬТАТОВ ЭКСПЕРИМЕНТОВ С ИЗОБРАЖЕНИЯМИ
# ============================================================================

print("\n" + "="*80)
print("Pav. 1.3 Eksperimento su statiniais vaizdais rezultatų lentelė")
print("="*80)

formats = ['BMP', 'JPG', 'PNG', 'TIF']
types = ['Color', 'Gray']

# Инициализация переменных
all_data = []
exp_numbers = []

# Собираем данные
if os.path.exists(experiment_folder):
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
        # Заголовок таблицы
        print("\n" + "-"*120)
        print(f"{'Bandymo Nr.':<12} {'Formatas':<10} {'Tipas':<10} {'Rezoliucija':<15} {'Kanalų kiekis':<15} {'Failo dydis (MB)':<20}")
        print("-"*120)
        
        # Данные по экспериментам
        all_data = []
        
        for exp_num in exp_numbers:
            for fmt in formats:
                for typ in types:
                    filename = f"Exp{exp_num}_{fmt}_{typ}"
                    
                    ext_map = {
                        'BMP': '.bmp',
                        'JPG': '.jpg',
                        'PNG': '.png',
                        'TIF': '.tif'
                    }
                    
                    ext = ext_map.get(fmt, '.jpg')
                    filepath = os.path.join(experiment_folder, filename + ext)
                    
                    if os.path.exists(filepath):
                        try:
                            img = Image.open(filepath)
                            width, height = img.size
                            resolution = f"{width}x{height}"
                            
                            if img.mode == 'RGB':
                                channels = 3
                            elif img.mode == 'L':
                                channels = 1
                            elif img.mode == 'RGBA':
                                channels = 4
                            else:
                                channels = len(img.getbands())
                            
                            file_size = Path(filepath).stat().st_size
                            size_mb = round(file_size / 1e6, 3)
                            
                            typ_lt = "Spalvotas" if typ == "Color" else "Pilkas"
                            
                            print(f"{exp_num:<12} {fmt:<10} {typ_lt:<10} {resolution:<15} {channels:<15} {size_mb:<20}")
                            
                            all_data.append({
                                'exp': exp_num,
                                'format': fmt,
                                'type': typ,
                                'resolution': resolution,
                                'channels': channels,
                                'size_mb': size_mb
                            })
                        except Exception as e:
                            pass
        
        print("-"*120)
        
        # Средние значения
        print("\n" + "="*80)
        print("VIDURKIAI (Spalvotos nuotraukos)")
        print("="*80)
        print(f"{'Formatas':<10} {'Vidutinis dydis (MB)':<25} {'Min (MB)':<15} {'Max (MB)':<15}")
        print("-"*70)
        
        for fmt in formats:
            sizes = [d['size_mb'] for d in all_data if d['format'] == fmt and d['type'] == 'Color']
            if sizes:
                avg = round(sum(sizes) / len(sizes), 3)
                min_size = round(min(sizes), 3)
                max_size = round(max(sizes), 3)
                print(f"{fmt:<10} {avg:<25} {min_size:<15} {max_size:<15}")
        
        print("\n" + "="*80)
        print("VIDURKIAI (Pilkos nuotraukos)")
        print("="*80)
        print(f"{'Formatas':<10} {'Vidutinis dydis (MB)':<25} {'Min (MB)':<15} {'Max (MB)':<15}")
        print("-"*70)
        
        for fmt in formats:
            sizes = [d['size_mb'] for d in all_data if d['format'] == fmt and d['type'] == 'Gray']
            if sizes:
                avg = round(sum(sizes) / len(sizes), 3)
                min_size = round(min(sizes), 3)
                max_size = round(max(sizes), 3)
                print(f"{fmt:<10} {avg:<25} {min_size:<15} {max_size:<15}")
    else:
        print("\n⚠ Eksperimentiniai failai nerasti")
else:
    print(f"\n⚠ Aplankas '{experiment_folder}' nerastas")

# ============================================================================
# 2. ТАБЛИЦА РЕЗУЛЬТАТОВ ЭКСПЕРИМЕНТОВ С ВИДЕО
# ============================================================================

print("\n\n" + "="*80)
print("Pav. 2.1 Eksperimento su video failais rezultatų lentelė")
print("="*80)

cv2 = None  # Инициализация переменной

if os.path.exists(video_folder):
    try:
        import cv2
        
        video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.flv'))]
        
        if video_files:
            print("\n" + "-"*120)
            print(f"{'Formatas':<15} {'Rezoliucija':<15} {'FPS':<8} {'Kadrų sk.':<12} {'Trukmė (s)':<12} {'Failo dydis (MB)':<20}")
            print("-"*120)
            
            for video_file in sorted(video_files):
                video_path = os.path.join(video_folder, video_file)
                format_name = video_file.replace('Video_', '').rsplit('.', 1)[0]
                
                cap = cv2.VideoCapture(video_path)
                
                if cap.isOpened():
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = int(cap.get(cv2.CAP_PROP_FPS))
                    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    duration = round(frame_count / fps, 2) if fps > 0 else 0
                    
                    file_size = Path(video_path).stat().st_size
                    size_mb = round(file_size / 1e6, 3)
                    
                    resolution = f"{width}x{height}"
                    
                    print(f"{format_name:<15} {resolution:<15} {fps:<8} {frame_count:<12} {duration:<12} {size_mb:<20}")
                    
                    cap.release()
            
            print("-"*120)
        else:
            print("\n⚠ Video failai nerasti")
    
    except ImportError:
        print("\n⚠ OpenCV neįdiegtas. Negalima analizuoti video failų")
        print("Įdiekite: pip install opencv-contrib-python")
else:
    print(f"\n⚠ Aplankas '{video_folder}' nerastas")

# ============================================================================
# 3. СОХРАНЕНИЕ В CSV ДЛЯ ИМПОРТА В EXCEL
# ============================================================================

print("\n\n" + "="*80)
print("IŠSAUGOJIMAS Į CSV FAILĄ")
print("="*80)

try:
    # Таблица 1: Изображения
    csv_images = "results_images.csv"
    with open(csv_images, 'w', encoding='utf-8') as f:
        f.write("Bandymo_Nr,Formatas,Tipas,Rezoliucija,Kanalu_kiekis,Failo_dydis_MB\n")
        
        if all_data:  # Проверка что данные есть
            for d in all_data:
                typ_lt = "Spalvotas" if d['type'] == "Color" else "Pilkas"
                f.write(f"{d['exp']},{d['format']},{typ_lt},{d['resolution']},{d['channels']},{d['size_mb']}\n")
    
    print(f"✓ Nuotraukų duomenys išsaugoti: {csv_images}")
    
    # Таблица 2: Видео
    csv_videos = "results_videos.csv"
    if os.path.exists(video_folder) and cv2 is not None:
        with open(csv_videos, 'w', encoding='utf-8') as f:
            f.write("Formatas,Rezoliucija,FPS,Kadru_sk,Trukme_s,Failo_dydis_MB\n")
            
            video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.flv'))]
            
            for video_file in sorted(video_files):
                video_path = os.path.join(video_folder, video_file)
                format_name = video_file.replace('Video_', '').rsplit('.', 1)[0]
                
                cap = cv2.VideoCapture(video_path)
                if cap.isOpened():
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = int(cap.get(cv2.CAP_PROP_FPS))
                    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    duration = round(frame_count / fps, 2) if fps > 0 else 0
                    file_size = Path(video_path).stat().st_size
                    size_mb = round(file_size / 1e6, 3)
                    resolution = f"{width}x{height}"
                    
                    f.write(f"{format_name},{resolution},{fps},{frame_count},{duration},{size_mb}\n")
                    cap.release()
        
        print(f"✓ Video duomenys išsaugoti: {csv_videos}")
    
    print("\n📊 CSV failus galite atidaryti Excel programoje!")
    
except Exception as e:
    print(f"⚠ Klaida saugant CSV: {e}")

print("\n" + "="*80)
print("✓ UŽBAIGTA")
print("="*80)