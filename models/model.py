import numpy as np
import h5py
import time
import os
import logging
import traceback
import tensorflow as tf
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_model(X, FLAGS):
	#ch, row, col = 3, 160, 320
	#Add the lambda here. Is it a mean substraction?

	conv1 = tf.layers.conv2d(
		tf.reshape(X,[FLAGS.batch,3,160,320]),
		filters = 16,
		kernel_size = (8,8),
		strides=(4, 4),
		padding='same',
		kernel_initializer=tf.contrib.layers.xavier_initializer(),
		bias_initializer=tf.zeros_initializer(),
		kernel_regularizer=None,
		name = 'conv1',
		activation = tf.nn.elu
		)

	conv2 = tf.layers.conv2d(
		conv1 ,
		filters = 32,
		kernel_size = (5,5),
		strides=(2, 2),
		padding='same',
		kernel_initializer=tf.contrib.layers.xavier_initializer(),
		bias_initializer=tf.zeros_initializer(),
		kernel_regularizer=None,
		name = 'conv2',
		activation = tf.nn.elu
		)

	conv3 = tf.layers.conv2d(
		conv2,
		filters = 64,
		kernel_size = (5,5),
		strides=(2, 2),
		padding='same',
		kernel_initializer=tf.contrib.layers.xavier_initializer(),
		bias_initializer=tf.zeros_initializer(),
		kernel_regularizer=None,
		name = 'conv3',
		activation = None
		)

	f1 = tf.contrib.layers.flatten(conv3)
	d1 = tf.nn.dropout(f1, FLAGS.dropout_rate1)
	e1 = tf.nn.elu(d1)
	dense1 = tf.layers.dense(e1, units = FLAGS.fc_dim)
	d2 = tf.nn.dropout(dense1, FLAGS.dropout_rate2)
	e2 = tf.nn.elu(d2)	
	dense2 = tf.layers.dense(e2, units = 1)

	return dense2


def get_loss(predictions,labels):
	# loss = tf.nn.l2_loss(predictions-labels)
	loss = tf.reduce_mean(tf.square(predictions-labels))
	return loss


def variable_summaries(var):
 	"""Attach a lot of summaries to a Tensor (for TensorBoard visualization).
	credits: https://www.tensorflow.org/get_started/summaries_and_tensorboard
 	"""
 	with tf.name_scope('summaries'):
		mean = tf.reduce_mean(var)
		tf.summary.scalar('mean', mean)
		with tf.name_scope('stddev'):
			stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
		tf.summary.scalar('stddev', stddev)
		tf.summary.scalar('max', tf.reduce_max(var))
		tf.summary.scalar('min', tf.reduce_min(var))
		tf.summary.histogram('histogram', var)