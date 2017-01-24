# coding=utf-8

'''
numpy中的newaxis
'''

import numpy as np

a = np.array([1,2,3])
print(a)
b = a[:,np.newaxis]
print(b)
c = a[np.newaxis,:]
print(c)
d = a[np.newaxis,np.newaxis]
print(d)
'''
[1 2 3]

[[1]
 [2]
 [3]]

[[1 2 3]]

[[[1 2 3]]]
'''
