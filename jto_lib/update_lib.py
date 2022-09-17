import os
import shutil
import subprocess
import sys


working_dir = '.'
lib_name = 'jto'


print('Remove previous build directories')
for filename in os.listdir(working_dir):
    if filename in ['build', 'dist'] or '.egg-info' in filename:
        print(f'Remove directory {filename}')
        shutil.rmtree(filename)

print('Build library')
subprocess.Popen([sys.executable, os.path.join(working_dir, 'setup.py'), "bdist_wheel"]).wait()

print(f'Unistall current version of library from interpreter')
subprocess.Popen(["pip", "uninstall", lib_name, "-y"]).wait()

print(f'Install library to current interpreter')
all_files = os.listdir(os.path.join(working_dir, 'dist'))
matching_file = [file for file in all_files if file.find('.whl')][0]
subprocess.Popen(["pip", "install", os.path.join(working_dir, 'dist', matching_file)]).wait()
