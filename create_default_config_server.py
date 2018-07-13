import os
from pathlib import Path
from shutil import copyfile


def create_config_if_needed():
    f_config = Path('./srv/conf.ini')
    if f_config.is_file():
        exit()
    else:
        copyfile('./utils/conf_server.ini', './srv/conf.ini')
        os.rename('./srv/conf_server.ini', './srv/conf.ini')


def main():
    create_config_if_needed()


if __name__ == '__main__':
    main()
