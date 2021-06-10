# distutils: language = c++

from ci_tessapi_wrapper cimport CITessApiWrapper


cdef class PyCITessApiWrapper:
    cdef CITessApiWrapper citaw
    
    def __cinit__(self):
        self.citaw = CITessApiWrapper()
        
    def image_to_string(self, lang, img, width_pixels, height_pixels, psm=3, resolution=96):
        output = ""
        
        if lang == "eng":
            self.citaw.eng_image_to_string()
        elif lang == "gs":
            self.citaw.gs_image_to_string()
        
        return output