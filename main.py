import os

from PIL import Image


def main():
    # compress_img("image/35x45mm-passport-photo-example.jpg")
    for file in os.listdir("image"):
        compress_img(f"image/{file}")


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def compress_img(image_name, new_size_ratio=1.0, quality=90, width=None, height=None, to_jpg=True):
    # загрузить изображение в память
    img = Image.open(image_name)
    print("[*] File name:", image_name.split("/")[1])
    
    # распечатать исходную форму изображения
    print("[*] Image shape:", img.size)
    
    # получить исходный размер изображения в байтах
    image_size = os.path.getsize(image_name)
    # распечатать размер перед сжатием/изменением размера
    print("[*] Size before compression:", get_size_format(image_size))
    
    if new_size_ratio < 1.0:
        # если коэффициент изменения размера ниже 1,0, умножьте ширину и высоту на этот коэффициент, чтобы уменьшить размер изображения.
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
        # распечатать новую форму изображения
        print("[+] New Image shape:", img.size)
    elif width and height:
        # если ширина и высота установлены, вместо этого измените размер с ними
        img = img.resize((width, height), Image.ANTIALIAS)
        # распечатать новую форму изображения
        print("[+] New Image shape:", img.size)
        
    # разделить имя файла и расширение
    filename, ext = os.path.splitext(image_name.split("/")[1])
    # сделать новое имя файла, добавив _compressed к исходному имени файла
    directory = os.path.dirname("./new_image/")
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    if to_jpg:
        # изменить расширение на JPEG
        new_filename = f"{directory}/{filename}.jpg"
    else:
        # сохранить то же расширение исходного изображения
        new_filename = f"{directory}/{filename}{ext}"
    try:
        # сохраняем изображение с соответствующим качеством и установите для оптимизации значение True
        img.save(new_filename, quality=quality, optimize=True, progressive=True)
    except OSError:
        # сначала преобразовать изображение в режим RGB
        img = img.convert("RGB")
        # повторим сохранение
        img.save(new_filename, quality=quality, optimize=True, progressive=True)
        
    print("[+] New file saved:", new_filename)
    
    # получить новый размер изображения в байтах
    new_image_size = os.path.getsize(new_filename)
    # распечатать новый размер в хорошем формате
    print("[+] Size after compression:", get_size_format(new_image_size))
    
    if new_image_size > image_size:
        os.remove(new_filename)
        print("[+] New file remove:", new_filename)
    else:
        # вычислить байты сохранения
        saving_diff = new_image_size - image_size
        # распечатать процент экономии
        print(f"[+] Image size change: {saving_diff/image_size*100:.2f}% of the original image size.")
        
    print("-------------------------------------------------------------------------------------\n")


if __name__ == '__main__':
    main()
