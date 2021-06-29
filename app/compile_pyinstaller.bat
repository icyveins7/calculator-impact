pyinstaller ci_app_main.py --hidden-import="skimage.filters.rank.core_cy_3d"                                           

mkdir dist\tesseract_custom
copy ..\tesseract_custom\* dist\tesseract_custom\*

mkdir dist\ci_app_main\platforms
copy dist\ci_app_main\PySide2\plugins\platforms\* dist\ci_app_main\platforms\*

copy *.png dist\ci_app_main\*

xcopy scripts\templates dist\ci_app_main\scripts\templates /E /H /C /I
