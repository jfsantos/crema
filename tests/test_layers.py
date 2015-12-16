#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''Tests for model layers'''

import numpy as np
import scipy
import scipy.stats
import tensorflow as tf
from nose.tools import eq_

import crema


def test_conv2_layer():

    def __test(shape, n_filters, nl, strides, mode, squeeze):
        # Our input batch
        x = np.random.randn(20, 5, 5, 7)

        x_in = tf.placeholder(tf.float32, shape=x.shape, name='x')

        output = crema.model.layers.conv2_layer(x_in, shape, n_filters,
                                                nonlinearity=nl,
                                                strides=strides,
                                                mode=mode,
                                                squeeze_dims=squeeze)

        with tf.Session() as sess:
            sess.run(tf.initialize_all_variables())
            y = sess.run(output, feed_dict={x_in: x})


        s1, s2 = x.shape[1:3]

        if mode == 'VALID':
            s1 = s1 - shape[0] + 1
            s2 = s2 - shape[1] + 1

        if strides is not None:
            s1 = s1 // strides[0] + (s1 % strides[0])
            s2 = s2 // strides[1] + (s2 % strides[1])

        target_shape = [x.shape[0], s1, s2, n_filters]

        if squeeze is not None:
            target_shape = [target_shape[_] for _ in range(4) if _ not in squeeze]

        eq_(y.shape, tuple(target_shape))

    # And a couple of squeeze tests
    yield __test, [5, 1], 3, tf.nn.relu, None, 'VALID', [1]
    yield __test, [1, 5], 3, tf.nn.relu, None, 'VALID', [2]

    for shape in [[1,3], [3, 3], [5, 1]]:
        for n_filters in [1, 2, 3]:
            for nl in [tf.nn.relu, tf.nn.relu6, tf.nn.tanh, None]:
                for strides in [None, [min(min(shape), 2), min(min(shape), 2)]]:
                    for mode in ['SAME', 'VALID']:
                        yield __test, shape, n_filters, nl, strides, mode, None


