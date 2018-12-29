import os
import zipfile

from spider.utils import file_utils


def zip_dir(path: str, output_file: str) -> None:
    """
    zip files from path into zip file
    :param path: path to directory
    :param output_file: output zip file
    :return: None
    """
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(path):
            for file in files:
                zip_file.write(os.path.join(root, file))


def unzip_file(file_name: str, output_dir: str) -> dict:
    """
    unzips file to output directory
    :param file_name: zip file name
    :param output_dir: output directory
    :return: structure of unzipped file as dictionary
    """
    file_utils.create_dir_if_not_exist(output_dir)
    with zipfile.ZipFile(file_name, 'r') as f:
        f.extractall(output_dir)
        files = [elem for elem in os.walk(output_dir)][0]
        return {
            'root': files[0],
            'dirs': files[1],
            'files': files[2]
        }
