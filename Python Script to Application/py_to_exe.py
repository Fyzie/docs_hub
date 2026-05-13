### Python script with Qt GUI
On Windows terminal:
```
python -m nuitka --standalone --show-progress --enable-plugin=pyside6 --include-qt-plugins=platforms,imageformats --noinclude-qt-plugins=qml,quick,charts,datavisualization,graphs --windows-console-mode=disable script_name.py
```
