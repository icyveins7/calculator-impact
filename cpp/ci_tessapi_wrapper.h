#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <stdint.h>

class CITessApiWrapper
{
    private:
        tesseract::TessBaseAPI *engapi;
        tesseract::TessBaseAPI *gsapi;
    
    public:
        CITessApiWrapper(){
            engapi = new tesseract::TessBaseAPI();
            // Initialize tesseract-ocr with English, without specifying tessdata path
            if (engapi->Init(NULL, "eng", tesseract::OEM_TESSERACT_ONLY)) { // this is --oem 0 -l eng
                fprintf(stderr, "Could not initialize tesseract ENG.\n");
                throw(1);
            }
            
            gsapi = new tesseract::TessBaseAPI();
            // Initialize tesseract-ocr with English, without specifying tessdata path
            if (gsapi->Init(NULL, "gs", tesseract::OEM_TESSERACT_ONLY)) { // this is --oem 0 -l gs
                fprintf(stderr, "Could not initialize tesseract GS.\n");
                throw(2);
            }
        }
        ~CITessApiWrapper(){
            engapi->End();
            delete engapi;
            gsapi->End();
            delete gsapi;
        }
        
        void eng_image_to_string(uint32_t *img, uint32_t width_pixels, uint32_t height_pixels,
                                 uint32_t depth, char *output, int psm=3) // 3 is the default
        {
            // memory for image
            Pix *image;
            // memory for text
            char *outText;
            
            image = pixCreate(width_pixels, height_pixels, depth);
            memcpy(image->data, img, width_pixels*height_pixels*sizeof(uint32_t));
            // OCR Result
            engapi->SetPageSegMode(psm);
            outText = engapi->GetUTF8Text();
            // copy into output
            strncpy(output, outText, strlen(outText) + 1);
            
            // free everything
            delete [] outText;
            pixDestroy(&image);
        }
        
        void gs_image_to_string(uint32_t *img, uint32_t width_pixels, uint32_t height_pixels,
                                uint32_t depth, char *output, int psm=3) // 3 is the default
        {
            // memory for image
            Pix *image;
            // memory for text
            char *outText;
            
            image = pixCreate(width_pixels, height_pixels, depth);
            memcpy(image->data, img, width_pixels*height_pixels*sizeof(uint32_t)); // copy into the allocated memory
            // OCR Result
            gsapi->SetPageSegMode(psm);
            outText = gsapi->GetUTF8Text();
            // copy into output
            strncpy(output, outText, strlen(outText) + 1);
            
            // free everything
            delete [] outText;
            pixDestroy(&image);
        }
}