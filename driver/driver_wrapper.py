from ctypes import *
#from comedi import *

mylib = CDLL("./libdriver.so")

print(mylib.main())


