# Declare the class with cdef
cdef extern from "ci_tessapi_wrapper.h":
    cdef cppclass CITessApiWrapper:
        CITessApiWrapper() except +
        void eng_image_to_string(unsigned char *, unsigned int, unsigned int,
                                 char *, int, int)
        void gs_image_to_string(unsigned char *, unsigned int, unsigned int,
                                 char *, int, int)