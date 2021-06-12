# distutils: language = c++

from ci_tessapi_wrapper cimport CITessApiWrapper

from libcpp.string cimport string

cdef class PyCITessApiWrapper:
    cdef CITessApiWrapper citaw
    
    # def __cinit__(self):
    #     print("Attempting to init..")
    #     self.citaw = CITessApiWrapper()
        
    def image_to_string(self, lang, img, width_pixels, height_pixels, psm=3, resolution=96):
        cdef string output
        
        if lang == "eng":
            output = self.citaw.eng_image_to_string(img, width_pixels, height_pixels, psm, resolution)
        elif lang == "gs":
            output = self.citaw.gs_image_to_string(img, width_pixels, height_pixels, psm, resolution)
        
        return output