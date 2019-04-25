# -*- coding: utf-8 -*-
import os
import re
import shutil
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--dst_config_dir', type=str,
                    default='',
                    help='dir which generate config files by multi-level directories.')
parser.add_argument('--config_dir', type=str,
                    default='',
                    help='dir which store config files.')

args = parser.parse_args()


def generate_dirs():
    for config_file in os.listdir(args.config_dir):
        # pat_result = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]+', config_file)[0]
        pat_result = re.findall(r'[^\.]+', config_file)[0]
        pat_result = re.findall(r'((.(?!_lukou))*.)', pat_result)
        pat_result = pat_result[0][0]

        dst_dir = os.path.join(args.dst_config_dir, pat_result)

        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)

        shutil.copy(src=os.path.join(args.config_dir, config_file),
                    dst=os.path.join(args.dst_config_dir, pat_result, config_file))


if __name__ == '__main__':
    generate_dirs()
