# !/usr/bin/python

# Dynamically change the content of modular-interlinking.{lang}.md files within path

import os
import shutil

def format_content():
    for root, dirs, files in os.walk(os.path.join('./'), topdown=True):
        for filename in files:
            if filename.startswith('modular-interlinking.') and filename.endswith('.md'):
            # if filename.startswith('modular-interlinking.es.md') and filename.endswith('.md'):
                read_content(os.path.join(root, filename))

def read_content(filePath):
    openFile = open(filePath,'r')
    title = None;
    for line in openFile.readlines():
        line = line.replace('\n', '')
        if line.startswith('title:'):
            if "interlinking" in line:
                title = line.replace('title:', '').replace('\'', '').replace('\n', '').replace(' ', '')
            else:
                raise Exception('File: %s doesn\'t have proper title name, found "%s"' % (filePath, line))

    if title:
        write_title(filePath, title)
    else:
        raise Exception('File: %s: unknown error happened.' % (filePath))

def write_title(filePath, title):
    print ('WRITING:  "%s"    ON FILE:    %s' % (title, filePath))
    content = "---\ntitle: "+title+"\n---"
    openFile = open(filePath,'w')
    openFile.write(content)

try:
    format_content()
except Exception as error:
    print('Error: {0}'.format(str(error)))
