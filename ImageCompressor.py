import logging
import os
from PIL import Image


class ImageCompressor:
    def __init__(self, image_dir):
        self.image_dir = image_dir

    @staticmethod
    def get_size_format(b, factor=1024, suffix="B"):
        """
        Scale bytes to its proper byte format
        e.g:
            1253656 → '1.20 MB'
            1253656678 → '1.17 GB'
        """
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}{unit}{suffix}"
            b /= factor
        return f"{b:.2f}Y{suffix}"

    def compress_img(self, image_name: str, new_size_ratio: float = 1.0, quality: int = 90, width: int = None,
                     height: int = None, to_jpg: bool = True):
        """
            Compresses an image with specified options and saves the compressed image.

            Args:
                image_name (str): The name of the image file to be compressed.
                new_size_ratio (float, optional): The ratio by which the image size will be reduced. Defaults to 1.0.
                quality (int, optional): The quality of the compressed image. Defaults to 90.
                width (int, optional): The width of the compressed image. Defaults to None.
                height (int, optional): The height of the compressed image. Defaults to None.
                to_jpg (bool, optional): Specifies whether to save the compressed image as a JPEG file. Defaults to True.
            """

        img = Image.open(image_name)
        logging.info(f'[*] File name: {image_name.split("/")[1]}')
        logging.info(f'[*] Image shape: {img.size}')

        image_size = os.path.getsize(image_name)
        logging.info(f'[*] Size before compression: {self.get_size_format(image_size)}')

        if new_size_ratio < 1.0:
            img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
            logging.info(f'[+] New Image shape: {img.size}')
        elif width and height:
            img = img.resize((width, height), Image.ANTIALIAS)
            logging.info("[+] New Image shape:", img.size)

        filename, ext = os.path.splitext(image_name.split("/")[1])
        directory = os.path.dirname("./new_image/")

        if not os.path.exists(directory):
            os.makedirs(directory)
        if to_jpg:
            new_filename = f"{directory}/{filename}.jpg"
        else:
            new_filename = f"{directory}/{filename}{ext}"
        try:
            img.save(new_filename, quality=quality, optimize=True, progressive=True)
        except OSError:
            img = img.convert("RGB")
            img.save(new_filename, quality=quality, optimize=True, progressive=True)

        logging.info(f'[+] New file saved: {new_filename}')
        new_image_size = os.path.getsize(new_filename)
        logging.info(f'[+] Size after compression: {self.get_size_format(new_image_size)}')

        if new_image_size > image_size:
            os.remove(new_filename)
            logging.info(f'[+] New file remove: {new_filename}'
                         f'\n-------------------------------------------------------------------------------------\n')
        else:
            saving_diff = new_image_size - image_size
            logging.info(f'[+] Image size change: {saving_diff / image_size * 100:.2f}% of the original image size. '
                         f'\n-------------------------------------------------------------------------------------\n')

    def run(self):
        """
        Run compresses all the images in the specified directory.
        """
        for file in os.listdir(self.image_dir):
            self.compress_img(f"{self.image_dir}/{file}")
