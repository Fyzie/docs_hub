## Python script with Qt GUI
Activate the environment and run below at the script directory to build the application:
```
python -m nuitka --standalone --show-progress --enable-plugin=pyside6 --include-qt-plugins=platforms,imageformats --noinclude-qt-plugins=qml,quick,charts,datavisualization,graphs --windows-console-mode=disable script_name.py
```

For PySide6, you might need to copy plugins from your environment folder to generated .dist folder.   
1. Go to `miniconda3\envs\{environment_name}\Lib\site-packages\PySide6\plugins` (the path may be different for individuals)
2. Copy all folders within the plugins
3. Paste the folders to qt-plugins of PySide6 in your generated .dist folder (usually at where you run the build command)
4. Run .exe in the .dist folder

### Alternate Cases
#### Case 1:   
1. PySide6 with Camera Driver
```
python -m nuitka --standalone --enable-plugin=pyside6 --windows-console-mode=disable --include-qt-plugins=platforms,imageformats --include-package=core --include-package=ui --include-data-dir=resources=resources --output-dir=dist main.py
```
