import os
from pathlib import Path
from shutil import copyfile


def create_config_if_needed():
    f_config = Path('./client_sms/conf.ini')
    if f_config.is_file():
        exit()
    else:
        copyfile('./utils/conf_client.ini', './client_sms/conf.ini')
        os.rename('./client_sms/conf_client.ini', './client_sms/conf.ini')


def main():
    create_config_if_needed()


if __name__ == '__main__':
    main()
