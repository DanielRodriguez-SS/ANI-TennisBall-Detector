from PIL import Image
from pillow_heif import register_heif_opener
import os
import shutil

PATH_TO_ORIGINALS_WITH_BALL = 'images/with_ball/originals'
PATH_TO_ORIGINALS_WITHOUT_BALL = 'images/without_ball/originals'
PATH_TO_COPIES_WITH_BALL = 'images/with_ball/copies_jpg'
PATH_TO_COPIES_WITHOUT_BALL = 'images/without_ball/copies_jpg'

paths = {'with balls': {
                        'originals' : PATH_TO_ORIGINALS_WITH_BALL,
                        'copies' : PATH_TO_COPIES_WITH_BALL},
         'without balls': {
                            'originals' : PATH_TO_ORIGINALS_WITHOUT_BALL,
                            'copies' : PATH_TO_COPIES_WITHOUT_BALL}
        }

def convert_heic_to_jpg(source_image_path:str, output_image_path:str) -> None:
    register_heif_opener()
    file_name = source_image_path.split('/')[-1].split('.')[-2]
    image = Image.open(source_image_path)
    image.convert('RGB').save(f'{output_image_path}/{file_name}.jpg')

def get_all_files_names_from_dir(path:str) -> list[str]:
    files = os.listdir(path)
    return files

def remove_all_files_on_dir(path:str) -> None:
    files_on_dir = get_all_files_names_from_dir(path)
    if files_on_dir:
        for file in files_on_dir:
            os.remove(f'{path}/{file}')

def get_non_jpg_files(path:str) -> list[str]:
    files = get_all_files_names_from_dir(path)
    non_jpg_files = []
    if files:
        for file in files:
            if 'jpg' in file.lower():
                continue
            non_jpg_files.append(file)
    return non_jpg_files

def get_jpg_files(path:str) -> list[str]:
    files = get_all_files_names_from_dir(path)
    jpg_files = []
    if files:
        for file in files:
            if 'jpg' in file.lower():
                jpg_files.append(file)
    return jpg_files

def copy_file_to_dir(source_file_path:str, destination_dir_path:str):
    shutil.copy2(source_file_path,destination_dir_path)

def file_images_refinement(path:dict):
    remove_all_files_on_dir(path['copies'])
    non_jpg_files = get_non_jpg_files(path['originals'])
    for file in non_jpg_files:
        convert_heic_to_jpg(f"{path['originals']}/{file}",path['copies'])
    jpg_files = get_jpg_files(path['originals'])
    for file in jpg_files:
        copy_file_to_dir(f"{path['originals']}/{file}",path['copies'])     

def main():
    file_images_refinement(paths['with balls'])
    file_images_refinement(paths['without balls'])