# Declare the class with cdef
cdef extern from "ci_tessapi_wrapper.h":
    cdef cppclass CITessApiWrapper:
        CITessApiWrapper() except +
        