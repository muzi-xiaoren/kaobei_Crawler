import os
import shutil

def move_images_to_main_folder(main_folder):
    # 获取主文件夹中的所有子文件夹
    subfolders = [f.path for f in os.scandir(main_folder) if f.is_dir()]
    
    for subfolder in subfolders:
        # 获取子文件夹中的所有图片文件
        images = [f for f in os.listdir(subfolder)]
        
        for image in images:
            src_path = os.path.join(subfolder, image)
            dest_path = os.path.join(main_folder, image)
            
            # 移动图片文件到主文件夹
            shutil.move(src_path, dest_path)
            # print(f'Moved {src_path} to {dest_path}')

# 使用示例
main_folder = '迷宮干'
move_images_to_main_folder(main_folder)
