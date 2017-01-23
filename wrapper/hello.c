#include "stdio.h"
#include "python2.7/Python.h"

char * hello(char * what){
return what;
}

static PyObject * hello_wrapper(PyObject * self, PyObject * args)
{
  char * input;
  char * result;
  PyObject * ret;

  // parse arguments
  if (!PyArg_ParseTuple(args, "s", &input)) {
    return NULL;
  }

  // run the actual function
  result = hello(input);

  // build the resulting string into a Python object.
  ret = PyString_FromString(result);
  free(result);

  return ret;
}

static PyMethodDef HelloMethods[] = {
 { "hello", hello_wrapper, METH_VARARGS, "Say hello" },
 { NULL, NULL, 0, NULL }
};

DL_EXPORT(void) inithello(void)
{
  Py_InitModule("hello", HelloMethods);
}

void main(){
	printf("HEi\n");
}



//http://intermediate-and-advanced-software-carpentry.readthedocs.io/en/latest/c++-wrapping.html
//gcc test.c -L /usr/lib/python2.7/config -l python2.7 -o main
// DEnne kommentaren la jeg til for å teste GitHub