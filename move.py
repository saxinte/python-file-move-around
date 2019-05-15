# !/usr/bin/python

import os
import shutil

folders_to_run = ['apprendre-espagnol-en-ligne',
'aprenda-espanhol-online',
'aprender-espanol-online',
'impara-spagnolo-online',
'nauka-hiszpanskiego-online',
'online-spanisch-lernen',
'uchit-ispanskij-online']
final_destination = 'learn-spanish-online'
exclude_files = ['.DS_Store']

def move_folders_page(folders, destination):
    for folder in folders:
        print('------- FOLDER PAGE --------')
        move_folder_page(folder, destination)
        print('------- FOLDER CONTENT --------')
        move_folder_content(folder, destination)
        print('------- CLEAN FOLDER --------')
        removeEmptyFolders(os.path.join('./', folder))

def move_file_to_folder(filePath, destinationFolder):

    # check if destination is a folder
    if os.path.isdir(destinationFolder):

        # check if file already exist in destination
        filename = os.path.split(filePath)[1];
        exists = os.path.isfile(os.path.join(destinationFolder, filename))
        if not exists:
            print('Moving %s to %s') % (filePath, destinationFolder)
            shutil.move(filePath, destinationFolder)
        else:
            raise Exception("File {0} already exist in destination {1}".format(str(filePath), str(destinationFolder)))
    else:
        raise Exception('Destination directory is not a folder.')


def move_folder_page(folder, destinationFolder):
    for root, dirs, files in os.walk(os.path.join('./', folder), topdown=False):

        # loop through each files down the folder
        for filename in files:

            if filename in exclude_files:
                continue;

            # variables
            filePath = os.path.join(root, filename)
            parentDirectoryName = os.path.split(os.path.dirname(filePath))[1]
            newDestination = os.path.join('./', destinationFolder)

            # if file is modular.{lang}.md and not within a _{xx} folder
            if filename.startswith('modular.') and filename.endswith('.md') and not parentDirectoryName.startswith('_'):
                move_file_to_folder(filePath, newDestination);



def move_folder_content(folder, destinationFolder):
    for root, dirs, files in os.walk(os.path.join('./', folder), topdown=False):

        # loop through each files down the folder
        for filename in files:
            if filename in exclude_files:
                continue;

            # variables
            filePath = os.path.join(root, filename)
            parentDirectoryName = os.path.split(os.path.dirname(filePath))[1]

            # find files within sub folders only (_)
            if parentDirectoryName.startswith('_'):

                # check if folder already exist in destination
                newDestination = os.path.join('./', destinationFolder, parentDirectoryName)
                exist = os.path.isdir(newDestination)
                if exist:
                    move_file_to_folder(filePath, newDestination)
                else:
                    raise Exception("Folder {0} does not exist in destination {1}".format(str(os.path.join('./', folder, parentDirectoryName)), str(os.path.join('./', destinationFolder))))

def removeEmptyFolders(path, removeRoot=False):

    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for filename in files:
            fullpath = os.path.join(path, filename)
            if os.path.isdir(fullpath):
                removeEmptyFolders(fullpath, True)
            else:
                if filename == '.DS_Store':
                    os.remove(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and removeRoot:
        print "Removing empty folder:", path
        os.rmdir(path)

try:
    move_folders_page(folders_to_run, final_destination)
except Exception as error:
    print("Error found: {0}".format(str(error)))
