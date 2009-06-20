/* floydwarshall.i */
%module floydwarshall
%include "carrays.i"
%array_functions(double, doubleArray);
%array_functions(int,    intArray);
%{
/* Put header files here or function declarations like below */
void floydwarshall(int n, double* m_adj, double* dist, int* pred);
%}
%include floydwarshall.cpp
