import csv
import os
import shutil
from datetime import date
from pathlib import Path, PurePath
from tkinter import filedialog
from tkinter import *

curr_date = date.today()

# Path to the working directory
def select_dir():
    root = Tk()
    root.filename =  filedialog.askdirectory(title = "Select directory")
    return root.filename

# Function moves files with certain file extension to given folder
def move_files_w_exts(csv_path, working_dir):
    existing_dirs = set()

    for directory in Path(working_dir).iterdir():
        if directory.is_dir():
            existing_dirs.add(directory)

    dirs_to_create = {}

    # Read csv file containing ['file extension', 'destination folder']
    with open(csv_path, newline='') as file:
        exts_dict = csv.DictReader(file)

        for row in exts_dict:
            dirs_to_create[row['File extension']] = row['Target directory']

        for dir_path in existing_dirs:
            # Iterating through every existing folder in working_dir to create folders with names specified in csv file
            for dir_name in dirs_to_create:
                path = Path(dir_path) / Path(dirs_to_create[dir_name])

                if not Path.exists(path):
                    Path.mkdir(path)

    # Move files from whole directory tree to folder specified in csv file -> Dict key
    for directory in existing_dirs:

        for key in dirs_to_create:
            file_list = Path(directory).glob(f'**/*{key}')

            for f in file_list:
                destination_path = Path(directory) / dirs_to_create[key]
                copy_dest_path = destination_path / f.name

                if not Path(copy_dest_path).exists():
                    shutil.copy(f, copy_dest_path)

                    new_filename = f.stem + " " + dir_path.stem + f.suffix
                    target_file_path = destination_path / new_filename

                    os.rename(copy_dest_path, target_file_path)
                    # os.remove(destination_path / f.name)


# Output present file extensions in given Path
def list_f_extensions(dir_path):
    home_dir = Path(dir_path)
    exts = set()

    # Iterate through files in given directory, if file is not a dir then add to list which is sorted before return
    for ext in home_dir.glob('**/*'):
        if ext.is_file():
            exts.add(str(ext.suffix))

    exts = sorted(exts)
    return exts


# Function reads folder names in given directory, then sorts data and writes it to a csv file called "clients.csv"
def dir_names_list(dir_path):
    home_dir = Path(dir_path)
    # Iterating through all folders and adding them to folders list
    folders = Path.iterdir(home_dir)

    clt_table = set()

    # To get only the name from the Path, stem method is used
    for folder_name in folders:
        clt_table.add(str(folder_name.stem))

    sorted_clt_tbl = sorted(clt_table)

    # Opening csv file in write mode to then add folder names from sorted list
    with open("clients.csv", "w", encoding="utf-8", newline="\n") as clt_csv:
        datawriter = csv.writer(clt_csv, dialect="excel")

        for clt in sorted_clt_tbl:
            datawriter.writerow([clt])


def template_dir_copy(dir_path):
    template_dir = PurePath("E:/Hobby/Roldam GIS Helper/RolDam/Nowy_klient")

    clt_name = input("Imię właściciela gospodarstwa: ")
    clt_sname = input("Nazwisko właściciela gospodarstwa: ")
    clt_town = input("Miejscowość siedziby gospodarstwa: ")

    folder_name = clt_sname + " " + clt_name + " - " + clt_town

    if input("Czy stworzyć folder o nazwie: " + folder_name + " ").lower()[0] == 't':
        # Checking if path is valid and client folder already exists
        # if not Path.exists(Path(curr_dir / folder_name)):
        #     # Copies contents of folder template_dir to "curr_dir + folder_name"
        shutil.copytree(template_dir, dir_path / folder_name, dirs_exist_ok=True)

        # Change of home directory to shorten "Path"
        os.chdir(dir_path / folder_name)
        print(os.getcwd())
        # Check if current year and month directories exist if not creating them
        if not Path.exists(Path(str(curr_date.year))):
            base = Path('ROK')
            target = Path(str(curr_date.year))
            base.rename(target)
        # else:
        #     Path.rmdir(Path('Rok'))

        if not Path.exists(Path(str(curr_date.year)) / str(curr_date.month)):
            base = Path(str(curr_date.year)) / 'MIESIAC'
            target = Path(str(curr_date.year)) / str(curr_date.month)
            base.rename(target)
        # else:
        #     Path.rmdir('Miesiac')
