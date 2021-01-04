from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('Matplotlib')
datas = collect_data_files('Matplotlib', subdir=None, include_py_files=True)