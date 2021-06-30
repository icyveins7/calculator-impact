set PYSIDE2_PLUGINS=H:\Python\Python39\envs\calcapp\Lib\site-packages\PySide2\plugins

pyinstaller ci_app_main.py --hidden-import="skimage.filters.rank.core_cy_3d" --add-binary="%PYSIDE2_PLUGINS%\styles;styles" --add-binary="%PYSIDE2_PLUGINS%\platformthemes;platformthemes" --add-binary="%PYSIDE2_PLUGINS%\platforms;platforms" --exclude-module PyQt5 %1

mkdir dist\tesseract_custom
copy ..\tesseract_custom\* dist\tesseract_custom\*

REM mkdir dist\ci_app_main\platforms
REM copy dist\ci_app_main\PySide2\plugins\platforms\* dist\ci_app_main\platforms\*

copy *.png dist\ci_app_main\*

xcopy scripts\templates dist\ci_app_main\scripts\templates /E /H /C /I
