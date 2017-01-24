import tensorflow as tf
#import numpy as np

a = tf.constant([1, 2, 3, 4, 5, 6], shape=[2, 3])
b = tf.constant([7, 8, 9, 10, 11, 12], shape=[3, 2])
c = tf.matmul(a, b)

sess = tf.Session()
result = sess.run([a,b])
print result
sess.close()


