# !/usr/bin/python

import os
import shutil
import random

# Grav themes templates root path
base_path_templates = './themes/busuu/templates/'

# Grav pages root path
base_path_pages = './pages/'

# All modules example folder path
base_path_final_destination = './pages/modulars/'

# Modulars to not add in the page
modular_ignore_list = ['modular-zendesk']


# Copy a given source folder over a destination
def copy_folder_over_destination(source, destination):
    shutil.copytree(source, destination)


# Returns an Array with all the  available modular names
def get_available_modules():
    temp_array = []
    for root, dirs, files in os.walk(os.path.join(base_path_templates, 'modular'), topdown=False):
        for filename in files:
            if filename.endswith('.html.twig'):
                modular_name = filename.split('.')[0] # converts `modular-name.twig.html` to `modular-name`
                if(not modular_name in modular_ignore_list):
                    temp_array.append(modular_name) # store it
    return temp_array


# Returns an array of all the files (paths)
# from the Grav pages folder and shuffle it
def get_all_files():
    all_files = []
    for root, dirs, files in os.walk(base_path_pages, topdown=False):
        for filename in files:
            filepath = os.path.join(root, filename)
            all_files.append(filepath)
    random.shuffle(all_files)
    return all_files


# Indicates wether or not a file is a modular type
# using the parent folder name as indicator
def is_file_modular(filename, parent_directory_foldername):
    return filename.startswith('modular-') and filename.endswith('.md') and parent_directory_foldername.startswith('_')


# Loop through all the files over the Grav pages
# then find modulars that exist in the available modulars
# then copy them over the final folder destination
def copy_modulars_folder_over_destination():

    print('--- SEARCH FOR MODULARS TO COPY ---\n')
    folder_name_index = 0
    available_modules = get_available_modules()
    all_files = get_all_files()

    # loop through each files down the folder
    for filepath in all_files:
        filename = os.path.basename(filepath)
        parent_directory_path = os.path.dirname(filepath)
        parent_directory_foldername = os.path.split(parent_directory_path)[1]

        # Avoid parsing destination in loop
        if base_path_final_destination in filepath:
            continue;
        
        # if file is not a modular stop here
        if not is_file_modular(filename, parent_directory_foldername):
            continue;
        
        # converts `modular-name.en.md` to `modular-name`
        modular_name = filename.split('.')[0]

        # if modular exist in the modular list then copy
        # the parent directory over destination 
        if modular_name in available_modules:
            folder_name_index += 1
            destinationFolderPath = os.path.join(base_path_final_destination, '_{0}'.format(str(folder_name_index)))
            print('-------')
            print('MODULE FOUND:   %s' % (modular_name))
            print('MODULE PATH:    %s' % (parent_directory_path))

            # copy the whole modular folder
            copy_folder_over_destination(parent_directory_path, destinationFolderPath)

            # ..then ensure the modular is removed from available list to avoid duplication
            available_modules.remove(modular_name)
            
    print('\n--- MODULARS COPIED! --- \n')


# Recursively deletes a folder and his content
def removeFolderAndChildrens(path, cleanRoot = False, removeSelf = False):

    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for filename in files:
            fullpath = os.path.join(path, filename)
            if os.path.isdir(fullpath):
                removeFolderAndChildrens(fullpath, True, True)
            elif cleanRoot:
                os.remove(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and removeSelf:
        # print ('Removing empty folder: %s' % path)
        os.rmdir(path)


# Main Execution
try:
    removeFolderAndChildrens(base_path_final_destination)
    copy_modulars_folder_over_destination()

except Exception as error:
    print('Error found: {0}'.format(str(error)))
