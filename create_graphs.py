try:
    from PIL import Image
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Для сохранения без отображения
except ImportError:
    print("Установите библиотеки:")
    print("  pip install Pillow matplotlib")
    exit()

import os
from pathlib import Path

# Настройка шрифтов для литовского языка
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (12, 6)

experiment_folder = "experiment_images"
video_folder = "experiment_videos"
graphs_folder = "graphs"
os.makedirs(graphs_folder, exist_ok=True)

print("="*80)
print("KŪRIMAS GRAFIKŲ")
print("="*80)

formats = ['BMP', 'JPG', 'PNG', 'TIF']
types = ['Color', 'Gray']

# Сбор данных
all_data = []

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
    
    for exp_num in exp_numbers:
        for fmt in formats:
            for typ in types:
                filename = f"Exp{exp_num}_{fmt}_{typ}"
                ext_map = {'BMP': '.bmp', 'JPG': '.jpg', 'PNG': '.png', 'TIF': '.tif'}
                ext = ext_map.get(fmt, '.jpg')
                filepath = os.path.join(experiment_folder, filename + ext)
                
                if os.path.exists(filepath):
                    try:
                        img = Image.open(filepath)
                        file_size = Path(filepath).stat().st_size
                        size_mb = round(file_size / 1e6, 3)
                        
                        all_data.append({
                            'exp': exp_num,
                            'format': fmt,
                            'type': typ,
                            'size_mb': size_mb
                        })
                    except:
                        pass

# ============================================================================
# GRAFIKAS 1: Spalvotų nuotraukų dydžiai (visi eksperimentai)
# ============================================================================

print("\n1. Spalvotų nuotraukų dydžiai...")

color_data = [d for d in all_data if d['type'] == 'Color']

if color_data:
    plt.figure(figsize=(14, 7))
    
    for fmt in formats:
        fmt_data = [d for d in color_data if d['format'] == fmt]
        if fmt_data:
            exps = [d['exp'] for d in fmt_data]
            sizes = [d['size_mb'] for d in fmt_data]
            plt.plot(exps, sizes, marker='o', linewidth=2, markersize=8, label=fmt)
    
    plt.xlabel('Bandymo numeris', fontsize=12, fontweight='bold')
    plt.ylabel('Failo dydis (MB)', fontsize=12, fontweight='bold')
    plt.title('Statinių spalvotų vaizdų dydžių priklausomybė nuo formato tipo', 
              fontsize=14, fontweight='bold', pad=20)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    graph1 = os.path.join(graphs_folder, 'grafikas_1_spalvoti.png')
    plt.savefig(graph1, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Išsaugota: {graph1}")

# ============================================================================
# GRAFIKAS 2: Pilkų nuotraukų dydžiai (visi eksperimentai)
# ============================================================================

print("\n2. Pilkų nuotraukų dydžiai...")

gray_data = [d for d in all_data if d['type'] == 'Gray']

if gray_data:
    plt.figure(figsize=(14, 7))
    
    for fmt in formats:
        fmt_data = [d for d in gray_data if d['format'] == fmt]
        if fmt_data:
            exps = [d['exp'] for d in fmt_data]
            sizes = [d['size_mb'] for d in fmt_data]
            plt.plot(exps, sizes, marker='s', linewidth=2, markersize=8, label=fmt)
    
    plt.xlabel('Bandymo numeris', fontsize=12, fontweight='bold')
    plt.ylabel('Failo dydis (MB)', fontsize=12, fontweight='bold')
    plt.title('Statinių pilkų vaizdų dydžių priklausomybė nuo formato tipo', 
              fontsize=14, fontweight='bold', pad=20)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    graph2 = os.path.join(graphs_folder, 'grafikas_2_pilki.png')
    plt.savefig(graph2, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Išsaugota: {graph2}")

# ============================================================================
# GRAFIKAS 3: Vidurkiai spalvotoms nuotraukoms
# ============================================================================

print("\n3. Vidurkiai (spalvotos nuotraukos)...")

if color_data:
    averages = []
    for fmt in formats:
        sizes = [d['size_mb'] for d in color_data if d['format'] == fmt]
        if sizes:
            averages.append(round(sum(sizes) / len(sizes), 3))
        else:
            averages.append(0)
    
    plt.figure(figsize=(10, 7))
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    bars = plt.bar(formats, averages, color=colors, edgecolor='black', linewidth=1.5)
    
    # Значения над столбцами
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f} MB', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.xlabel('Formatas', fontsize=12, fontweight='bold')
    plt.ylabel('Vidutinis failo dydis (MB)', fontsize=12, fontweight='bold')
    plt.title('Statinių spalvotų vaizdų dydžių vidurkiai', 
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    
    graph3 = os.path.join(graphs_folder, 'grafikas_3_vidurkiai_spalvoti.png')
    plt.savefig(graph3, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Išsaugota: {graph3}")

# ============================================================================
# GRAFIKAS 4: Vidurkiai pilkoms nuotraukoms
# ============================================================================

print("\n4. Vidurkiai (pilkos nuotraukos)...")

if gray_data:
    averages = []
    for fmt in formats:
        sizes = [d['size_mb'] for d in gray_data if d['format'] == fmt]
        if sizes:
            averages.append(round(sum(sizes) / len(sizes), 3))
        else:
            averages.append(0)
    
    plt.figure(figsize=(10, 7))
    colors = ['#95a5a6', '#34495e', '#7f8c8d', '#bdc3c7']
    bars = plt.bar(formats, averages, color=colors, edgecolor='black', linewidth=1.5)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f} MB', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.xlabel('Formatas', fontsize=12, fontweight='bold')
    plt.ylabel('Vidutinis failo dydis (MB)', fontsize=12, fontweight='bold')
    plt.title('Statinių pilkų vaizdų dydžių vidurkiai', 
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    
    graph4 = os.path.join(graphs_folder, 'grafikas_4_vidurkiai_pilki.png')
    plt.savefig(graph4, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Išsaugota: {graph4}")

# ============================================================================
# GRAFIKAS 5: Video failų ir jų statinių vaizdų palyginimas
# ============================================================================

print("\n5. Video failų palyginimas...")

if os.path.exists(video_folder):
    try:
        import cv2
        
        video_sizes = []
        video_formats = []
        
        video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.flv'))]
        
        for video_file in sorted(video_files):
            video_path = os.path.join(video_folder, video_file)
            format_name = video_file.replace('Video_', '').rsplit('.', 1)[0]
            
            file_size = Path(video_path).stat().st_size
            size_mb = round(file_size / 1e6, 3)
            
            video_sizes.append(size_mb)
            video_formats.append(format_name)
        
        if video_sizes:
            plt.figure(figsize=(10, 7))
            colors = ['#e74c3c', '#3498db', '#9b59b6', '#f39c12']
            bars = plt.bar(video_formats, video_sizes, color=colors[:len(video_formats)], 
                          edgecolor='black', linewidth=1.5)
            
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.3f} MB', ha='center', va='bottom', 
                        fontsize=11, fontweight='bold')
            
            plt.xlabel('Video formatas', fontsize=12, fontweight='bold')
            plt.ylabel('Failo dydis (MB)', fontsize=12, fontweight='bold')
            plt.title('Video failų dydžių palyginimas', 
                      fontsize=14, fontweight='bold', pad=20)
            plt.grid(True, axis='y', alpha=0.3)
            plt.tight_layout()
            
            graph5 = os.path.join(graphs_folder, 'grafikas_5_video.png')
            plt.savefig(graph5, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"   ✓ Išsaugota: {graph5}")
    
    except ImportError:
        print("   ⚠ OpenCV neįdiegtas - praleista")

print("\n" + "="*80)
print(f"✓ Visi grafikai išsaugoti aplanke '{graphs_folder}'")
print("="*80)
print("\n📊 Galite įterpti šiuos grafikus į savo ataskaitą!")