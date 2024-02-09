import re
import shutil
import os
import logging


def split_filepath(path):
    directory = path.split("\\")
    filename = directory.pop()
    return "\\".join(directory), filename


def move_file(initial_loc, final_dir) -> str | None:
    if initial_loc is None or final_dir is None:
        return None
    print(initial_loc)
    filename = split_filepath(initial_loc)[1]
    shutil.move(initial_loc, final_dir + "\\" + filename)
    logging.debug(f'Moved \"{filename}\" from '
                  f'\"{initial_loc}\" to \"{final_dir}\"')
    return final_dir + "\\" + filename


def rename_file(initial_loc, new_name):
    path = split_filepath(initial_loc)
    initial_filename = path[1]
    final_loc = path[0] + "\\" + new_name

    os.rename(initial_loc, final_loc)
    logging.debug(f'Renamed {initial_filename} to {new_name}')
    return final_loc


def replace(string: str, replace_pattern: str, replace_with: str) -> str:
    return re.sub(replace_pattern, replace_with, string)
