# Calculator Impact

A Pyside2 (Qt) application that calculates and compares your [Genshin Impact](https://genshin.mihoyo.com) characters' stats via drag-and-drop of screenshots (rather than entering in the numbers manually)!

## Requirements
```bash
pip install pytesseract pillow scikit-image pyside2 numpy
```
##Folder organisation (for testing)

    .
    ├── calcutils                   # basic functions
    ├── workflow                    # main function to extract the required stat labels and values for further processing
    ├── string_filtering            # employing regex and other text processing to produce a dictionary of stats and their corresponding values
    ├── image_to_artifactdictionary # using the functions to link up dictionary to artifact classes
    ├── plus_button                 # plus button for reference
    ├── lockbutton2                 # lockbutton2 for reference
    ├── lockbutton                  # lockbutton for reference
    ├── imgs                        # folder to store all images
        ├── ss                      # where the uploaded full screenshots are saved
            ├── saves               # where the screenshots are snipped before processing


## Credits
Credits to Creamy Lam for her design of Xiangling's bear icon.
