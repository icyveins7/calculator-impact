# Calculator Impact

A Pyside2 (Qt) application that calculates and compares your [Genshin Impact](https://genshin.mihoyo.com) characters' stats via drag-and-drop of screenshots (rather than entering in the numbers manually)!

## Requirements
```bash
pip install pytesseract pillow scikit-image pyside2 numpy cython
```

The newest iteration which uses the tesseract API requires the tesseract and leptonica libraries. On linux this is done via

```bash
sudo apt-get install libtesseract4 libtesseract-dev
```

On Windows, please install [vcpkg](https://github.com/microsoft/vcpkg) and use that to install tesseract and leptonica. The official tesseract documentation contains the help needed.

## Folder organisation (for testing)

    CWD
    ├── calcutils.py                   # basic functions
    ├── workflow.py                    # main function to extract the required stat labels and values for further processing
    ├── string_filtering.py            # employing regex and other text processing to produce a dictionary of stats and their corresponding values
    ├── image_to_artifactdictionary.py # using the functions to link up dictionary to artifact classes
    ├── plus_button                    # plus button for reference
    ├── lockbutton2                    # lockbutton2 for reference
    ├── lockbutton                     # lockbutton for reference
    ├── imgs                           # folder to store all images
        ├── ss                         # where the uploaded full screenshots are saved

## Credits
Credits to Creamy Lam for her design of Xiangling's bear icon.
