import os
import shutil

def move_images_to_subfolders(main_folder):
    # 获取主文件夹中的所有图片文件
    images = [f for f in os.listdir(main_folder) if f.endswith('.webp') or f.endswith('.jpg') or f.endswith('.png')]
    
    for image in images:
        # 提取图片文件名中的子文件夹编号
        subfolder_number = image.split('_')[0]
        subfolder_path = os.path.join(main_folder, subfolder_number)
        
        # 如果子文件夹不存在，则创建
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        
        src_path = os.path.join(main_folder, image)
        dest_path = os.path.join(subfolder_path, image)
        
        # 移动图片文件到相应的子文件夹
        shutil.move(src_path, dest_path)
        # print(f'Moved {src_path} to {dest_path}')

# 使用示例
main_folder = '迷宮干'
move_images_to_subfolders(main_folder)
