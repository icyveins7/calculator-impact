#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <stdint.h>
#include <string>

class CITessApiWrapper
{
    private:
        tesseract::TessBaseAPI *engapi;
        tesseract::TessBaseAPI *gsapi;
    
    public:
    
        CITessApiWrapper(){
            printf("Allocating new engapi..\n");
            engapi = new tesseract::TessBaseAPI();
            // Initialize tesseract-ocr with English, without specifying tessdata path
            if (engapi->Init(NULL, "eng", tesseract::OEM_TESSERACT_ONLY)) { // this is --oem 0 -l eng
                printf("Could not initialize tesseract ENG.\n");
                throw(1);
            }
            
            printf("Allocating new gsapi..\n");
            gsapi = new tesseract::TessBaseAPI();
            // Initialize tesseract-ocr with GS, without specifying tessdata path
            if (gsapi->Init(NULL, "gs", tesseract::OEM_TESSERACT_ONLY)) { // this is --oem 0 -l gs
                printf("Could not initialize tesseract GS.\n");
                throw(2);
            }
        }
        ~CITessApiWrapper(){
            engapi->End();
            delete engapi;
            gsapi->End();
            delete gsapi;
        }
        
        std::string eng_image_to_string(unsigned char *img, uint32_t width_pixels, uint32_t height_pixels,
                                 int psm=3, int resolution=96)
        {
            // memory for text
            char *outText;
            
            // Set Image and Resolution
            engapi->SetImage(img, width_pixels, height_pixels, 3, 3*width_pixels);
            engapi->SetSourceResolution(resolution);
            // OCR Result
            engapi->SetPageSegMode(static_cast<tesseract::PageSegMode>(psm));
            outText = engapi->GetUTF8Text();
            // create output std string
            std::string output(outText);
            
            // free everything
            delete [] outText;
            
            return output;
        }
        
        std::string gs_image_to_string(unsigned char *img, uint32_t width_pixels, uint32_t height_pixels,
                                int psm=3, int resolution=96)
        {
            // memory for text
            char *outText;
            
            // Set Image and Resolution
            gsapi->SetImage(img, width_pixels, height_pixels, 3, 3*width_pixels);
            gsapi->SetSourceResolution(resolution);
            // OCR Result
            gsapi->SetPageSegMode(static_cast<tesseract::PageSegMode>(psm));
            outText = gsapi->GetUTF8Text();
            // create output std string
            std::string output(outText);
            
            // free everything
            delete [] outText;
            
            return output;
        }
};
