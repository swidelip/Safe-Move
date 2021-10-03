import colorama
import sys
import os
from time import time
from shutil import copyfile

if 'nt' in os.name: os.system('cls');
else: os.system('clear');

colorama.init(autoreset=True) 

c_colors = {
    'white': '\x1b[37m',
    'br_blue': '\x1b[34;1m',
    'br_red': '\x1b[31;1m'
}

c_mods = {
    'rs': '\x1b[0m',
    'bold': '\x1b[1m',
    'bbrb': '\x1b[1m\x1b[34;1m',
    'bbrr': '\x1b[1m\x1b[31;1m'
}

prefix = c_mods['bbrb'] + '{~}' + c_mods['rs']
wprefix = '{~}'
erprefix = c_mods['bbrr'] + '{~}' + c_mods['rs']

def printlogo():
    print('''\x1b[1m\x1b[34;1m
   _____        ,__                                            
  (        ___  /  `   ___       , _ , _     __.  _   __   ___ 
   `--.   /   ` |__  .'   `      |' `|' `. .'   \ |   /  .'   `
      |  |    | |    |----'      |   |   | |    | `  /   |----'
 \___.'  `.__/| |    `.___,      /   '   /  `._.'  \/    `.___,
                /                                              \x1b[0m''')

def askopen(title, filetypes):
    import tkinter as tk
    from tkinter import filedialog
    try:
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        a = filedialog.askopenfilename(title=title, filetypes=filetypes)
        root.destroy()
        return a
    except Exception as ex:
        print(f'\n\n{erprefix} Error at open file dialog: '+str(ex))
        quit()

def asksave(title, filetypes, initialfile):
    import tkinter as tk
    from tkinter import filedialog
    try:
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        a = filedialog.asksaveasfilename(title=title, filetypes=filetypes, initialfile=initialfile)
        root.destroy()
        return a
    except Exception as ex:
        print(f'\n\n{erprefix} Error at save file dialog: '+str(ex))
        quit()

def rewrite(path):
    try:
        with open(path, 'ba+') as f:
            length = f.tell()
            f.close()
        with open(path, 'br+') as f:
            f.seek(0)
            f.write(os.urandom(length))
            f.close()
        os.remove(path)
    except Exception as ex:
        print(f'\n\n{erprefix} Error at rewriting "{path}": '+str(ex))
        quit()

printlogo()
sys.stdout.write('\n{0} Select file to securely move: \n > '.format(prefix))
sys.stdout.flush()

usr_file_path = askopen(title='Select file to securely move', filetypes=(('All files', '*.*'), ('', '')))
if usr_file_path != '' and usr_file_path != None and os.path.exists(usr_file_path): sys.stdout.write(usr_file_path+'\n');
else: sys.stdout.write(c_mods['bbrr']+'None'+c_mods['rs']+'\n'); quit();

sys.stdout.write('\n{0} Select where securely move file: \n > '.format(prefix))
sys.stdout.flush()

usr_sfile_path = asksave(title='Select where securely move file', filetypes=(('All files', '*.*'), ('', '')), initialfile=usr_file_path)
if usr_sfile_path != '' and usr_sfile_path != None: sys.stdout.write(usr_sfile_path+'\n');
else: sys.stdout.write(c_mods['bbrr']+'None'+c_mods['rs']+'\n'); quit();

if usr_file_path == usr_sfile_path: print(f'\n{erprefix} Same files'); quit();

usr_ask = input(f'\n{prefix} Move "{usr_file_path}" to "{usr_sfile_path}" (Y/n): \n > ')
if 'y' not in usr_ask.lower() and 'н' not in usr_ask.lower(): quit();

start_time = time()
if os.path.exists(usr_sfile_path): rewrite(usr_sfile_path);
copyfile(usr_file_path, usr_sfile_path)
rewrite(usr_file_path)
end_time = time() - start_time

print(f'\n{prefix} Successfully moved: {end_time}')
