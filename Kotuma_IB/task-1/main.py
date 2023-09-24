import os

batch_size = 2

# Функция нахождения всех путей к файлам в каталоге
def get_path_to_files(path):
    os.chdir(path)
    path_to_files = []
    for dir_path, dir_names, file_names in os.walk(".", topdown=False):
        for name in file_names:
            path_to_files.append(os.path.join(dir_path, name))
    return path_to_files


# Функция нахождения ХЭШ-суммы файла
def get_hash_file(path):
    with open(path, 'rb') as file:
        batch = file.read(batch_size)
        cur_hash = batch
        while batch:  # Пока не дочитаем до конца файла
            batch = file.read(batch_size)
            if batch != b'':  # Если строка не байтовая, то сложение отрезка по xor
                if len(batch) < batch_size:
                    batch.zfill(batch_size)
                cur_hash = bytes(a ^ b for a, b in zip(cur_hash, batch))
    return cur_hash


path_to_folder_with_files = input('Путь до директории или BaseFolder: ') \
                            or './BaseFolder'

path_to_hash = './hash.txt'

state = int(input('1 - Подсчитать ХЭШ-сумму файлов\n2 - Проверить целостность каталога \n') or 1)

if state == 1:  # Подсчет хэш-суммы всех файлов каталога
    path_to_files = get_path_to_files(path_to_folder_with_files)
    hash_temp = ''
    for file_path in path_to_files:
        hash_temp += file_path + ' -- ' + str(get_hash_file(file_path)) + '\n'
    os.chdir('..')
    with open(path_to_hash, 'w') as file:
        file.write(hash_temp)
else:  # Проверка целостности каталога
    path_to_files = {}
    with open(path_to_hash, 'r') as file:
        lines = [line for line in file]
        for line in lines:
            t = line.replace('\n', '').split(' -- ')
            path_to_files[t[0]] = t[1]
    os.chdir(path_to_folder_with_files)

    changed_files = []
    for file in path_to_files:
        if os.path.exists(file) and str(get_hash_file(file)) != path_to_files[file]:
            changed_files.append(file)
    os.chdir('..')

    current_path_to_files = get_path_to_files(path_to_folder_with_files)
    deleted_files = list(set(list(path_to_files)).difference(set(current_path_to_files)))
    added_files = list(set(current_path_to_files).difference(set(list(path_to_files))))

    print('Изменённые файлы: ', *changed_files)
    print('Удалённые файлы: ', *deleted_files)
    print('Добавленные файлы: ', *added_files)
