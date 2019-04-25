# -*- coding: utf-8 -*-
import os
import random

import shutil

if __name__ == '__main__':
    src_dir = '/media/e/weizhang/test/BD/AgainstRedLight/0712/pass'

    dir_list = os.listdir(src_dir)

    name_list_norepeat = []
    name_dir_norepeat = []

    for item in dir_list:
        index = item.find('@')
        first_item = item[:index]
        if first_item not in name_list_norepeat:
            name_list_norepeat.append(first_item)
            name_dir_norepeat.append(item)


    out_dir = '/media/e/weizhang/test/BD/AgainstRedLight/0712/passselect/'

    for dir_name in name_dir_norepeat:
        dir_name = os.path.join(src_dir, dir_name)
        print dir_name
        imgs = os.listdir(dir_name)

        if len(imgs) == 0:
            continue
        elif len(imgs) == 1:
            shutil.copy(os.path.join(dir_name, imgs[0]), os.path.join(out_dir, imgs[0]))
            continue

        rand_num1 = random.randint(0, len(imgs) - 1)
        rand_num2 = random.randint(0, len(imgs) - 1)
        while rand_num1 == rand_num2:
            rand_num2 = random.randint(0, len(imgs) - 1)

        shutil.copy(os.path.join(dir_name, imgs[rand_num1]), os.path.join(out_dir, imgs[rand_num1]))
        shutil.copy(os.path.join(dir_name, imgs[rand_num2]), os.path.join(out_dir, imgs[rand_num2]))