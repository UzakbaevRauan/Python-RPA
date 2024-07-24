import os
from collections import defaultdict
import logging


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

def categorize_files_by_type(file_path):
    files = os.listdir(file_path)
    file_type = defaultdict(list)
    
    if not os.listdir(file_path):  # Проверка, если директория пуста
        file_type[''].append(file_path)
    else:
        for i in files:  # Проход по всем файлам и поддиректориям
            full_path = os.path.join(file_path, i)  # Формирование полного пути к файлу/директории
            logging.info(full_path)  # Логирование полного пути
            
            if os.path.isfile(full_path):  
                file_type[i.split('.')[-1].upper()].append(full_path)  # Добавление файла в словарь по его расширению
            else:
                # Если это директория, рекурсивный вызов для сканирования её содержимого
                sub_files = categorize_files_by_type(full_path)
                for ext, paths in sub_files.items():
                    file_type[ext].extend(paths)  # Объединение результатов из поддиректорий
    
    return file_type

def categorize_files_by_type_filter_by_size(file_path, file_size):
    file_size = int(file_size)
    files = os.listdir(file_path) 
    file_type = defaultdict(list)  
    
    if not os.listdir(file_path):  # Проверка, если директория пуста
        file_type[''].append(file_path)  
    else:
        for i in files: 
            full_path = os.path.join(file_path, i)  # Формирование полного пути к файлу/директории
            logging.info(full_path)  # Логирование полного пути
            
            if not os.path.isdir(full_path):  # Если это не директория, то это файл
                if os.path.getsize(full_path) > file_size:  # Фильтрация по размеру файла
                    file_type[i.split('.')[-1].upper()].append(full_path)  # Добавление файла в словарь по его расширению
            else:
                # Если это директория, рекурсивный вызов для сканирования её содержимого
                sub_files = categorize_files_by_type_filter_by_size(full_path, file_size)
                for ext, paths in sub_files.items():
                    for path in paths:
                        if os.path.getsize(path) > file_size:  # Фильтрация по размеру файла
                            file_type[ext].append(path)  # Добавление файла в словарь по его расширению
    
    return file_type

directory = input()
# file_size = input()

if os.path.isdir(directory):
    overall_map = categorize_files_by_type(directory)  # Без фильтрации
   #overall_map = categorize_files_by_type_filter_by_size(directory, file_size)  # С фильтрацией по размеру
    for key in overall_map:
        print(f"'.{key}' : {overall_map[key]}") 
else:
    print('Такой папки нет')
