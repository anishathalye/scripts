#!/usr/bin/env python3

import subprocess
import os
import multiprocessing


def main() -> None:
    all_files = os.listdir('.')
    with multiprocessing.Pool() as p:
        delete = p.map(is_live_photo, all_files)
    to_delete = [all_files[i] for i in range(len(all_files)) if delete[i]]
    confirm = input(f'delete {len(to_delete)} files? [y/N]: ')
    if confirm and confirm[0] == 'y':
        for file in to_delete:
            os.unlink(file)
        print('done')
    else:
        print('aborted')


def is_live_photo(filename: str) -> bool:
    if not filename.lower().endswith('.mov'):
        return False
    try:
        out = subprocess.check_output(['exiftool', '-LivePhotoAuto', filename], stderr=subprocess.DEVNULL)
        if b'Live Photo Auto' in out:
            return True
    except:
        pass
    return False


if __name__ == '__main__':
    main()
