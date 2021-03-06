# coding=utf-8
# View more python learning tutorial on my Youtube and Youku channel!!!

# Youtube video tutorial: https://www.youtube.com/channel/UCdyjiB5H8Pu7aDTNVXTTpcg
# Youku video tutorial: http://i.youku.com/pythontutorial
"""
softmax mnist 导出模型
Please note, this code is only for python 3+. If you are using python 2+, please modify the code accordingly.
"""
from __future__ import print_function
import tensorflow as tf
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import signature_def_utils
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.saved_model import utils
from tensorflow.examples.tutorials.mnist import input_data
from PIL import Image
import numpy as np
import cv2

work_dir = '/tmp/mnist_softmax/1'

# number 1 to 10 data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)


def add_layer(inputs, in_size, out_size, activation_function=None,):
    # add one more layer and return the output of this layer
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1,)
    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b,)
    return outputs


def compute_accuracy(v_xs, v_ys):
    # print(v_xs[0], v_ys[0])
    img_x = v_xs[4].reshape(28, 28) * 255
    image2 = Image.fromarray(img_x).convert('L')
    print(np.array(image2))
    image2.save('test_m.png')
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs})
    m_y_pre = tf.argmax(y_pre, 1)
    print(sess.run(m_y_pre, feed_dict={xs: v_xs, ys: v_ys}))
    correct_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(v_ys, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys})
    return result

# define placeholder for inputs to network
xs = tf.placeholder(tf.float32, [None, 784])  # 28x28
ys = tf.placeholder(tf.float32, [None, 10])

# add output layer
prediction = add_layer(xs, 784, 10,  activation_function=tf.nn.softmax)

# the error between prediction and real data
cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),
                                              reduction_indices=[1]))       # loss
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

sess = tf.Session()
# important step
# tf.initialize_all_variables() no long valid from
# 2017-03-02 if using tensorflow >= 0.12
if int((tf.__version__).split('.')[1]) < 12 and int((tf.__version__).split('.')[0]) < 1:
    init = tf.initialize_all_variables()
else:
    init = tf.global_variables_initializer()
sess.run(init)

for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys})
    if i % 1000 == 0:
        compute_accuracy(mnist.test.images, mnist.test.labels)
    # print(compute_accuracy(
    #     mnist.test.images, mnist.test.labels))

# im = Image.open('test_f_20.tiff')
# newImg = Image.new("RGB", (28, 28), (0, 0, 0)).convert('F')
# newImg.paste(im, (4, 4))
# newImg.save('test_f_28.tiff')

# gray_im_arr = np.array(im).reshape(784) / 255.0
# print(gray_im_arr)

# img_gray = cv2.imread('test.png', 0)
# img_dist = cv2.adaptiveThreshold(
#     img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 5)
# cv2.imwrite("test_cv.png", img_dist)


raise SystemExit

print('Exporting trained model to', work_dir)
builder = saved_model_builder.SavedModelBuilder(work_dir)

# Build the signature_def_map.

tensor_info_x = utils.build_tensor_info(xs)
tensor_info_y = utils.build_tensor_info(prediction)

prediction_signature = signature_def_utils.build_signature_def(
    inputs={'req_x': tensor_info_x},
    outputs={'res_y': tensor_info_y},
    method_name=signature_constants.PREDICT_METHOD_NAME)

legacy_init_op = tf.group(
    tf.initialize_all_tables(), name='legacy_init_op')
builder.add_meta_graph_and_variables(
    sess, [tag_constants.SERVING],
    signature_def_map={
        'predict_x':
            prediction_signature
    },
    legacy_init_op=legacy_init_op)

builder.save()

print('Done exporting!')
