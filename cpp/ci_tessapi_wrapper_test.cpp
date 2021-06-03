#include "ci_tessapi_wrapper.h"
#include <iostream>
#include <stdint.h>

int main(){
    const size_t imgsize = 40572;
    const uint32_t depth = 8;
    const uint32_t height_pixels = 42;
    const uint32_t width_pixels = 322;

    FILE *fp = fopen("testimg.bin","rb");
    uint32_t imgdata = (uint32_t)malloc(sizeof(uint32_t)*imgsize);
    fread(imgdata, sizeof(uint32_t), imgsize, fp);
    fclose(fp);

    // make the class
    CITessApiWrapper citaw;
    char txt[1024];
    citaw.eng_image_to_string(imgdata, width_pixels, height_pixels,
                                depth, txt);
    
    // cleanup
    free(imgdata);
}