# distutils: language = c++

from ci_tessapi_wrapper cimport CITessApiWrapper

from libcpp.string cimport string

cdef class PyCITessApiWrapper:
    cdef CITessApiWrapper citaw
    
    # def __cinit__(self):
    #     print("Attempting to init..")
    #     self.citaw = CITessApiWrapper()
        
    def image_to_string(self, lang, img, width_pixels, height_pixels, whitelist="", psm=3, resolution=96):
        cdef string output
        cdef string whitelist_string = whitelist.encode('UTF-8')
        
        if lang == "eng":
            output = self.citaw.eng_image_to_string(img, width_pixels, height_pixels, whitelist_string, psm, resolution)
        elif lang == "gs":
            output = self.citaw.gs_image_to_string(img, width_pixels, height_pixels, whitelist_string, psm, resolution)
        
        return output