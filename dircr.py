import os
import shutil

def creat_DIR_img():
    try:
        if not os.path.isdir('imageQR'):
            os.mkdir("imageQR")
            print('Есть')
            return 'Создано'
        return 'Уже сущ'
    except:
        return 'Ошибка создания'

def del_DIR_img():
    if os.path.isdir("imageQR"):
        shutil.rmtree("imageQR")
        print('Удалено')
        return 'Удвлено'
    print('НЕТ')
    return 'НЕТ'
del_DIR_img()