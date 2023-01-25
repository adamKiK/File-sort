import csv
import f_d_mgmt as mgmt
from pathlib import Path

curr_dir = Path("e:\Hobby\Roldam GIS Helper\RolDam\Klienci\Markefka")
working_dir = Path('e:\Hobby\Roldam GIS Helper\RolDam\Klienci\Markefka')


def main():
    # Save to csv file extensions present at directory [curr_dir]

    exts_list = mgmt.list_f_extensions(curr_dir)
    file_directories_dict = {}

    # Iterating through found file extensions, create dictionary with target directory added to each extension
    for record in exts_list:
        target_dir = str(input(f'Files with {record} extension to be placed in folder named: '))
        file_directories_dict[record] = target_dir

    with open('file_exts.csv', 'w', newline='') as exts_csv_file:
        fieldnames = ['File extension', 'Target directory']
        extensionsaver = csv.DictWriter(exts_csv_file, fieldnames=fieldnames)
        extensionsaver.writeheader()

        for key in file_directories_dict:
            extensionsaver.writerow({'File extension': key,'Target directory': file_directories_dict[key]})

    mgmt.move_files_w_exts('file_exts.csv', working_dir)





if __name__ == '__main__':
    main()
