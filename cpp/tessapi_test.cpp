#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <chrono>
#include <iostream>

int main()
{
    char *outText;

    auto t1 = std::chrono::high_resolution_clock::now();
    tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();
    // Initialize tesseract-ocr with English, without specifying tessdata path
    if (api->Init(NULL, "eng", tesseract::OEM_TESSERACT_ONLY)) {
        fprintf(stderr, "Could not initialize tesseract.\n");
        exit(1);
    }
    auto t2 = std::chrono::high_resolution_clock::now();
    std::cout<<"Time for initialization: " << std::chrono::duration<double>(t2-t1).count() << "s." << std::endl;

    // Open input image with leptonica library
    auto t3 = std::chrono::high_resolution_clock::now();
    Pix *image = pixRead("testimg.png");
    api->SetImage(image);
    printf("Width: %d\nHeight: %d\nDepth: %d\n", pixGetWidth(image), pixGetHeight(image), pixGetDepth(image));
    // Get OCR result
    outText = api->GetUTF8Text();
    auto t4 = std::chrono::high_resolution_clock::now();
    std::cout<<"Time for pixRead to result: " << std::chrono::duration<double>(t4-t3).count() << "s." << std::endl;
    printf("OCR output:\n%s", outText);
    
    // Open directly
    // FILE *fp = fopen("testimg.png", "rb");
//     unsigned char *imgdata = (unsigned char*)malloc(sizeof(unsigned char) * 18349);
//    fread(imgdata, sizeof(unsigned char), 18349, fp);
    FILE *fp = fopen("testimg.bin", "rb");
    unsigned char *imgdata = new unsigned char[40572];
    fread(imgdata, sizeof(unsigned char), 40572, fp);

    fclose(fp);
    api->SetImage(imgdata, 322, 42, 3, 3*322);
    api->SetSourceResolution(96);
    
    char *outText2 = api->GetUTF8Text(); // yay this works but there is a weird warning, need to set resolution (is 96,96 according to Pillow)
    
    printf("OCR output again: \n%s", outText2);
    
    delete outText2;

    // Destroy used object and release memory
    api->End();
    delete api;
    delete [] outText;
    pixDestroy(&image);

    return 0;
}
