# Unzip and Remove Unwanted Files on Linux

Navigate to the directory, run commands below:
```
unzip folder_name.zip
chmod -R 777 folder_name
find folder_name -name "filename" -type f -delete
```

`-R` = recursive (apply to all subfolders and files)

As `777` is full permission for everyone. For safer permissions, can use:
```
chmod -R 755 folder_name
```
