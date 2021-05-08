cimport scipy.special.cython_special as cs
from libc cimport math

cdef double _phi(double z) nogil:
    """evaluates the normal PDF. Used in `studentized range`"""
    cdef double inv_sqrt_2pi = 0.3989422804014327
    return inv_sqrt_2pi * math.exp(-0.5 * z * z)


cdef double _Phi(double z) nogil:
    """evaluates the normal CDF. Used in `studentized range`"""
    cdef double m_sqrt1_2 = 0.7071067811865475
    return 0.5 * math.erfc(-z * m_sqrt1_2)


cdef double genstudentized_range_cdf(int n, double[2] x, void *user_data) nogil:
    # evaluates the integrand of Equation (3) by Batista, et al [2]
    # destined to be used in a LowLevelCallable
    q = (<double *> user_data)[0]
    k = (<double *> user_data)[1]
    df = (<double *> user_data)[2]

    s = x[1]
    z = x[0]

    # harcoded constants to avoid useless log evals
    cdef double log_2 = 0.6931471805599453
    cdef double log_inv_sqrt_2pi = -0.9189385332046727

    # suitable terms are evaluated within logarithms to avoid under/overflows
    log_terms = (math.log(k) + (df / 2) * math.log(df)
                 - (math.lgamma(df / 2) + (df / 2 - 1) * log_2)
                 + (df - 1) * math.log(s) - (df * s * s / 2)
                 + log_inv_sqrt_2pi - 0.5 * z * z)  # Normal PDF

    # multiply remaining term outside of log because it can be 0
    return math.exp(log_terms) * math.pow(_Phi(z + q * s) - _Phi(z), k - 1)