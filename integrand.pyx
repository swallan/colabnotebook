cimport libc.math as math
cimport scipy.special.cython_special as cs

# direct translation from python
cdef double _phi(double z) nogil:
  """evaluates the normal PDF. Used in `studentized range`"""
  cdef double inv_sqrt_2pi = 0.3989422804014327
  return inv_sqrt_2pi * math.exp(-0.5 * z * z)

cdef double _Phi(double z) nogil:
  """evaluates the normal CDF. Used in `studentized range`"""
  return cs.ndtr(z)

cdef double inner(double s, double z, double q, double k, double nu) nogil:
  return _phi(z)*(_Phi(z+q*s)-_Phi(z))**(k-1)

cdef double outer(double s, double z, double q, double k, double nu) nogil:
  inner_int = inner(s, z, q, k, nu)
  return s**(nu)*_phi((nu ** .5)*s)*inner_int

cdef double genstudentized_range_cdf(int n, double * x, void *user_data) nogil:
    q = (<double *> user_data)[0]
    k = (<double *> user_data)[1]
    nu = (<double *> user_data)[2]

    s = x[1]
    z = x[0]
    return (((2 * math.M_PI)**.5)*k*nu**(nu/2) /
          (math.tgamma(nu/2)*2**(nu/2-1))*outer(s, z, q, k, nu))
