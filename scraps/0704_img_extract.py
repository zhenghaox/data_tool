# -*- coding: utf-8 -*-
import os
import random

import shutil

if __name__ == '__main__':
    src_dir = '/data_1/weizhang/data/红绿灯标注/0813/0813/'

    dir_list = os.listdir(src_dir)

    name_list_norepeat = []
    name_dir_norepeat = []

    for item in dir_list:
        index = item.find('@')
        first_item = item[:]
        if first_item not in name_list_norepeat:
            name_list_norepeat.append(first_item)
            name_dir_norepeat.append(item)

    print len(name_list_norepeat), len(name_dir_norepeat)

    out_dir = '/data_1/weizhang/data/红绿灯标注/0813/select'

    for dir_name in name_dir_norepeat:
        dir_name = os.path.join(src_dir, dir_name)
        if not os.path.isdir(dir_name):
            continue
        imgs = os.listdir(dir_name)

        if len(imgs) == 0:
            continue
        elif len(imgs) == 1:
            
            shutil.copy(os.path.join(dir_name, imgs[0]), os.path.join(out_dir, imgs[0]))
            continue

        rand_num1 = random.randint(0, len(imgs) - 1)
        rand_num2 = random.randint(0, len(imgs) - 1)
        # rand_num3 = random.randint(0, len(imgs) - 1)
        # rand_num4 = random.randint(0, len(imgs) - 1)
        # rand_num5 = random.randint(0, len(imgs) - 1)
        # rand_num6 = random.randint(0, len(imgs) - 1)
        # rand_num7 = random.randint(0, len(imgs) - 1)
        # rand_num8 = random.randint(0, len(imgs) - 1)
        # rand_num9 = random.randint(0, len(imgs) - 1)
        # rand_num10 = random.randint(0, len(imgs) - 1)
        # rand_num11 = random.randint(0, len(imgs) - 1)
        # rand_num12 = random.randint(0, len(imgs) - 1)
        while rand_num1 == rand_num2:
            rand_num2 = random.randint(0, len(imgs) - 1)

        shutil.move(os.path.join(dir_name, imgs[rand_num1]), os.path.join(out_dir, imgs[rand_num1]))
        shutil.move(os.path.join(dir_name, imgs[rand_num2]), os.path.join(out_dir, imgs[rand_num2]))
        # shutil.copy(os.path.join(dir_name, imgs[rand_num3]), os.path.join(out_dir, imgs[rand_num3]))
        # shutil.copy(os.path.join(dir_name, imgs[rand_num3]), os.path.join(out_dir, imgs[rand_num3]))
        # shutil.copy(os.path.join(dir_name, imgs[rand_num5]), os.path.join(out_dir, imgs[rand_num5]))
        # shutil.copy(os.path.join(dir_name, imgs[rand_num6]), os.path.join(out_dir, imgs[rand_num6]))
        # shutil.copy(os.path.join(dir_name, imgs[rand_num7]), os.path.join(out_dir, imgs[rand_num7]))
        # shutil.copy(os.path.join(dir_name, imgs[rand_num8]), os.path.join(out_dir, imgs[rand_num8]))
        # shutil.copy(os.path.join(dir_name, imgs[rand_num9]), os.path.join(out_dir, imgs[rand_num9]))
        # shutil.copy(os.path.join(dir_name, imgs[rand_num10]), os.path.join(out_dir, imgs[rand_num10]))
        # shutil.copy(os.path.join(dir_name, imgs[rand_num11]), os.path.join(out_dir, imgs[rand_num11]))
        # shutil.copy(os.path.join(dir_name, imgs[rand_num12]), os.path.join(out_dir, imgs[rand_num12]))
