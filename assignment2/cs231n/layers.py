import numpy as np


def affine_forward(x, w, b):
  """
  Computes the forward pass for an affine (fully-connected) layer.

  The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
  examples, where each example x[i] has shape (d_1, ..., d_k). We will
  reshape each input into a vector of dimension D = d_1 * ... * d_k, and
  then transform it to an output vector of dimension M.

  Inputs:
  - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
  - w: A numpy array of weights, of shape (D, M)
  - b: A numpy array of biases, of shape (M,)
  
  Returns a tuple of:
  - out: output, of shape (N, M)
  - cache: (x, w, b)
  """

  #############################################################################
  # TODO: Implement the affine forward pass. Store the result in out. You     #
  # will need to reshape the input into rows.                                 #
  #############################################################################
  out = np.dot(x.reshape(x.shape[0], -1), w) + b
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b)
  return out, cache


def affine_backward(dout, cache):
  """
  Computes the backward pass for an affine layer.

  Inputs:
  - dout: Upstream derivative, of shape (N, M)
  - cache: Tuple of:
    - x: Input data, of shape (N, d_1, ... d_k)
    - w: Weights, of shape (D, M)

  Returns a tuple of:
  - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
  - dw: Gradient with respect to w, of shape (D, M)
  - db: Gradient with respect to b, of shape (M,)
  """
  x, w, b = cache
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the affine backward pass.                                 #
  #############################################################################
  dx = np.dot(dout, w.T).reshape(x.shape)
  dw = np.dot(x.reshape(x.shape[0], -1).T, dout)
  db = np.sum(dout, axis=0)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def relu_forward(x):
  """
  Computes the forward pass for a layer of rectified linear units (ReLUs).

  Input:
  - x: Inputs, of any shape

  Returns a tuple of:
  - out: Output, of the same shape as x
  - cache: x
  """
 
  #############################################################################
  # TODO: Implement the ReLU forward pass.                                    #
  #############################################################################
  out = np.maximum(0, x)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = x
  return out, cache


def relu_backward(dout, cache):
  """
  Computes the backward pass for a layer of rectified linear units (ReLUs).

  Input:
  - dout: Upstream derivatives, of any shape
  - cache: Input x, of same shape as dout

  Returns:
  - dx: Gradient with respect to x
  """

  #############################################################################
  # TODO: Implement the ReLU backward pass.                                   #
  #############################################################################

  dx = (cache > 0)
  dx = dx * dout

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def batchnorm_forward(x, gamma, beta, bn_param):
  """
  Forward pass for batch normalization.
  
  During training the sample mean and (uncorrected) sample variance are
  computed from minibatch statistics and used to normalize the incoming data.
  During training we also keep an exponentially decaying running mean of the mean
  and variance of each feature, and these averages are used to normalize data
  at test-time.

  At each timestep we update the running averages for mean and variance using
  an exponential decay based on the momentum parameter:

  running_mean = momentum * running_mean + (1 - momentum) * sample_mean
  running_var = momentum * running_var + (1 - momentum) * sample_var

  Note that the batch normalization paper suggests a different test-time
  behavior: they compute sample mean and variance for each feature using a
  large number of training images rather than using a running average. For
  this implementation we have chosen to use running averages instead since
  they do not require an additional estimation step; the torch7 implementation
  of batch normalization also uses running averages.

  Input:
  - x: Data of shape (N, D)
  - gamma: Scale parameter of shape (D,)
  - beta: Shift paremeter of shape (D,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features

  Returns a tuple of:
  - out: of shape (N, D)
  - cache: A tuple of values needed in the backward pass
  """
  mode = bn_param['mode']
  eps = bn_param.get('eps', 1e-5)
  momentum = bn_param.get('momentum', 0.9)

  N, D = x.shape
  running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
  running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

  out, cache = None, None
  if mode == 'train':
    #############################################################################
    # TODO: Implement the training-time forward pass for batch normalization.   #
    # Use minibatch statistics to compute the mean and variance, use these      #
    # statistics to normalize the incoming data, and scale and shift the        #
    # normalized data using gamma and beta.                                     #
    #                                                                           #
    # You should store the output in the variable out. Any intermediates that   #
    # you need for the backward pass should be stored in the cache variable.    #
    #                                                                           #
    # You should also use your computed sample mean and variance together with  #
    # the momentum variable to update the running mean and running variance,    #
    # storing your result in the running_mean and running_var variables.        #
    #############################################################################
    ''' fast-version
      sample_mean = np.sum(x, axis=0) / float(N)
      sample_var = np.sum((x - sample_mean)**2, axis=0) / float(N)

      x_hat = (x - sample_mean) / np.sqrt(sample_var + eps)
      out = gamma * x_hat + beta

      cache = (x, N, sample_mean, sample_var, x_hat, gamma, beta, eps)
    '''

    # 1. sample mean, shape=(D, )
    sample_mean = np.sum(x, axis=0) / float(N)

    # 2. (x - sample_mean), shape=(N, D)
    x_mean = x - sample_mean

    # 3. x_mean square, shape=(N, D)
    x_mean_squ = x_mean ** 2

    # 4. sample_var, shape=(D, )
    sample_var = np.sum(x_mean_squ, axis=0) / float(N)

    # 5. sqrt(sample_var + eps), shape=(D, )
    sample_var_sqrt = (sample_var + eps) ** 0.5

    # 6. x_hat, shape=(N, D)
    x_hat = x_mean / sample_var_sqrt

    # 7. out, shape=(N, D)
    out = gamma * x_hat + beta

    # Store the updated running means back into bn_param
    bn_param['running_mean'] = momentum * running_mean + (1 - momentum) * sample_mean
    bn_param['running_var'] = momentum * running_var + (1 - momentum) * sample_var

    # cache for back prop
    cache = (x, N, sample_mean, x_mean, x_mean_squ, sample_var, sample_var_sqrt, x_hat, gamma, beta, eps)
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  elif mode == 'test':
    #############################################################################
    # TODO: Implement the test-time forward pass for batch normalization. Use   #
    # the running mean and variance to normalize the incoming data, then scale  #
    # and shift the normalized data using gamma and beta. Store the result in   #
    # the out variable.                                                         #
    #############################################################################
    x_hat = (x - running_mean) / np.sqrt(running_var + eps)
    out = gamma * x_hat + beta
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  else:
    raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

  return out, cache


def batchnorm_backward(dout, cache):
  """
  Backward pass for batch normalization.
  
  For this implementation, you should write out a computation graph for
  batch normalization on paper and propagate gradients backward through
  intermediate nodes.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, D)
  - cache: Variable of intermediates from batchnorm_forward.
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs x, of shape (N, D)
  - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
  - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
  """
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #############################################################################
  ''' fast-version
    (x, N, sample_mean, sample_var, x_hat, gamma, beta, eps) = cache

    # dL/dgamma = dL/dout * dout/dgamma = dout * x_hat
    dgamma = np.sum(x_hat * dout, axis=0)

    # dL/dbeta = dL/dout * dout/dbeta = dout * 1
    dbeta = np.sum(dout, axis=0)

    # set f(x) = sample_mean, g(x) = sample_var
    # dL/dx = dL/dout * dout/dx_hat * dx_hat/dx = dout * gamma * dx_hat/dx
    # dx_hat/dx = [(1 - df(x)/dx) * (g(x) + eps)^(1/2) + (x - f(x)) * 1/2 * (g(x) + eps)^(-1/2) * dg(x)/dx] / (g(x) + eps)
    # df(x)/dx = 1/m
    # dg(x)/dx = "2/m * (x - f(x))"

    f = sample_mean
    g = sample_var
    df = 1. / N
    dg = 2. / N * (x - f)
    dx = df * gamma * (g+eps)**(-0.5) * (N * dout - np.sum(dout, axis=0) - (x-f) / (g+eps) * np.sum(dout * (x-f), axis=0))
  '''

  (x, N, sample_mean, x_mean, x_mean_squ, sample_var, sample_var_sqrt, x_hat, gamma, beta, eps) = cache

  # 7. dgamma: shape=(D, ), dbeta: shape=(D, ), dx_hat: shape=(N, D)
  dgamma = np.sum(dout * x_hat, axis=0)
  dbeta = np.sum(dout, axis=0)
  dx_hat = dout * gamma

  # 6. dx_mean: shape=(N, D), dsample_var_sqrt: shape=(D, )
  dx_mean = dx_hat / sample_var_sqrt
  dsample_var_sqrt = np.sum(dx_hat * -1. * x_mean / (sample_var_sqrt**2.), axis=0)

  # 5. dsample_var: shape=(D, )
  dsample_var = dsample_var_sqrt * 0.5 * (sample_var + eps)**(-0.5)

  # 4. dx_mean_squ: shape=(N, D)
  dx_mean_squ = dsample_var * np.ones(x_mean_squ.shape) / float(N)

  # 3. dx_mean: shape=(N, D)
  dx_mean += dx_mean_squ * 2. * x_mean

  # 2. dx: shape=(N, D), dsample_mean: shape=(D, )
  dx = dx_mean
  dsample_mean = np.sum(dx_mean * -1., axis=0)

  # 1. dx, shape=(N, D)
  dx += dsample_mean * np.ones(x.shape) / float(N)

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta


def batchnorm_backward_alt(dout, cache):
  """
  Alternative backward pass for batch normalization.
  
  For this implementation you should work out the derivatives for the batch
  normalizaton backward pass on paper and simplify as much as possible. You
  should be able to derive a simple expression for the backward pass.
  
  Note: This implementation should expect to receive the same cache variable
  as batchnorm_backward, but might not use all of the values in the cache.
  
  Inputs / outputs: Same as batchnorm_backward
  """
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #                                                                           #
  # After computing the gradient with respect to the centered inputs, you     #
  # should be able to compute gradients with respect to the inputs in a       #
  # single statement; our implementation fits on a single 80-character line.  #
  #############################################################################
  (x, N, sample_mean, x_mean, x_mean_squ, sample_var, sample_var_sqrt, x_hat, gamma, beta, eps) = cache

  dgamma = np.sum(dout * x_hat, axis=0)
  dbeta = np.sum(dout, axis=0)
  f = sample_mean
  g = sample_var
  df = 1. / N
  dx = df * gamma * (g+eps)**(-0.5) * (N * dout - np.sum(dout, axis=0) - (x-f) / (g+eps) * np.sum(dout * (x-f), axis=0))
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  
  return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
  """
  Performs the forward pass for (inverted) dropout.

  Inputs:
  - x: Input data, of any shape
  - dropout_param: A dictionary with the following keys:
    - p: Dropout parameter. We drop each neuron output with probability p.
    - mode: 'test' or 'train'. If the mode is train, then perform dropout;
      if the mode is test, then just return the input.
    - seed: Seed for the random number generator. Passing seed makes this
      function deterministic, which is needed for gradient checking but not in
      real networks.

  Outputs:
  - out: Array of the same shape as x.
  - cache: A tuple (dropout_param, mask). In training mode, mask is the dropout
    mask that was used to multiply the input; in test mode, mask is None.
  """
  p, mode = dropout_param['p'], dropout_param['mode']
  if 'seed' in dropout_param:
    np.random.seed(dropout_param['seed'])

  mask = None
  out = None

  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase forward pass for inverted dropout.   #
    # Store the dropout mask in the mask variable.                            #
    ###########################################################################
    mask = np.random.rand(*x.shape) >= p
    out = x * mask / (1. - p)
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    ###########################################################################
    # TODO: Implement the test phase forward pass for inverted dropout.       #
    ###########################################################################
    out = x
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

  cache = (dropout_param, mask)
  out = out.astype(x.dtype, copy=False)

  return out, cache


def dropout_backward(dout, cache):
  """
  Perform the backward pass for (inverted) dropout.

  Inputs:
  - dout: Upstream derivatives, of any shape
  - cache: (dropout_param, mask) from dropout_forward.
  """
  dropout_param, mask = cache
  p = dropout_param['p']
  mode = dropout_param['mode']
  
  dx = None
  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase backward pass for inverted dropout.  #
    ###########################################################################
    dx = dout * mask / (1. - p)
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    dx = dout

  return dx


def conv_forward_naive(x, w, b, conv_param):
  """
  A naive implementation of the forward pass for a convolutional layer.

  The input consists of N data points, each with C channels, height H and width
  W. We convolve each input with F different filters, where each filter spans
  all C channels and has height HH and width HH.

  Input:
  - x: Input data of shape (N, C, H, W)
  - w: Filter weights of shape (F, C, HH, WW)
  - b: Biases, of shape (F,)
  - conv_param: A dictionary with the following keys:
    - 'stride': The number of pixels between adjacent receptive fields in the
      horizontal and vertical directions.
    - 'pad': The number of pixels that will be used to zero-pad the input.

  Returns a tuple of:
  - out: Output data, of shape (N, F, H', W') where H' and W' are given by
    H' = 1 + (H + 2 * pad - HH) / stride
    W' = 1 + (W + 2 * pad - WW) / stride
  - cache: (x, w, b, conv_param)
  """
  #############################################################################
  # TODO: Implement the convolutional forward pass.                           #
  # Hint: you can use the function np.pad for padding.                        #
  #############################################################################
  (N, C, H, W) = x.shape
  (F, C, HH, WW) = w.shape
  (F, ) = b.shape
  stride = conv_param['stride']
  pad = conv_param['pad']
  H_prime = 1 + (H + 2 * pad - HH) / stride
  W_prime = 1 + (W + 2 * pad - WW) / stride

  out = np.zeros((N, F, H_prime, W_prime))

  npad = ((0,), (0,), (pad,), (pad,))
  x_pad = np.pad(x, pad_width=npad, mode='constant', constant_values=0)

  for i in range(H_prime):
    for j in range(W_prime):
      hs, he = i*stride, i*stride+HH
      ws, we = j*stride, j*stride+WW
      tensor = x_pad[:, :, hs:he, ws:we].flatten()  # shape=(N * C * HH * WW)
      for k in range(F):
        shape = np.concatenate([[N],np.ones(len(w[k].shape))])  # shape=(N, 1, 1, 1)
        f = np.tile(w[k], shape).flatten()    # shape=(N * C * HH * WW)
        dot = tensor*f                        # shape=(N * C * HH * WW)
        Nsplit = np.split(dot, N)             # shape=(N, C * HH * WW)
        Nsum = np.sum(Nsplit, axis=1) + b[k]  # shape=(N, )
        out[:, k, i, j] = Nsum                # assign sum to out

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b, conv_param)
  return out, cache


def conv_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a convolutional layer.

  Inputs:
  - dout: Upstream derivatives.
  - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

  Returns a tuple of:
  - dx: Gradient with respect to x
  - dw: Gradient with respect to w
  - db: Gradient with respect to b
  """
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the convolutional backward pass.                          #
  # borrow from https://github.com/cthorey/CS231/                             #
  #############################################################################
  (x, weight, b, conv_param) = cache
  (N, C, H, W) = x.shape
  (F, C, HH, WW) = weight.shape
  (F, ) = b.shape
  stride = conv_param['stride']
  pad = conv_param['pad']
  H_prime = 1 + (H + 2 * pad - HH) / stride
  W_prime = 1 + (W + 2 * pad - WW) / stride

  npad = ((0,), (0,), (pad,), (pad,))
  x_pad = np.pad(x, pad_width=npad, mode='constant', constant_values=0)

  # db: shape=(F,)
  db = np.zeros(b.shape)
  for f in range(F):
    db[f] = np.sum(dout[:, f, :, :])

  # dw: shape(F, C, HH, WW)
  dw = np.zeros(weight.shape)
  for f in range(F):
    for c in range(C):
      for h in range(HH):
        for w in range(WW):
          x_loc = x_pad[:, c, h:h + H_prime * stride:stride, w:w + W_prime * stride:stride]  # shape=(N, H_prime, W_prime)
          dw[f, c, h, w] = np.sum(dout[:, f, :, :] * x_loc)

  # dx: shape=(N, C, H, W)
  dx = np.zeros(x.shape)
  for n in range(N):
    for f in range(F):
      for h in range(H):
        for w in range(W):
          for hp in range(H_prime):
            for wp in range(W_prime):
              mask1 = np.zeros_like(weight[f, :, :, :])  # shape=(C, HH, WW)
              mask2 = np.zeros_like(weight[f, :, :, :])  # shape=(C, HH, WW)
              if (h + pad - hp * stride) < HH and (h + pad - hp * stride) >= 0:
                mask1[:, h + pad - hp * stride, :] = 1.
              if (w + pad - wp * stride) < WW and (w + pad - wp * stride) >= 0:
                mask2[:, :, w + pad - wp * stride] = 1.
              dx[n, :, h, w] += dout[n, f, hp, wp] * np.sum(weight[f, :, :, :] * mask1 * mask2, axis=(1, 2))
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def max_pool_forward_naive(x, pool_param):
  """
  A naive implementation of the forward pass for a max pooling layer.

  Inputs:
  - x: Input data, of shape (N, C, H, W)
  - pool_param: dictionary with the following keys:
    - 'pool_height': The height of each pooling region
    - 'pool_width': The width of each pooling region
    - 'stride': The distance between adjacent pooling regions

  Returns a tuple of:
  - out: Output data
  - cache: (x, pool_param)
  """
  #############################################################################
  # TODO: Implement the max pooling forward pass                              #
  #############################################################################
  (N, C, H, W) = x.shape
  pool_h = pool_param['pool_height']
  pool_w = pool_param['pool_width']
  pool_s = pool_param['stride']

  H_prime = 1 + (H - pool_h) / pool_s
  W_prime = 1 + (W - pool_w) / pool_s

  out = np.zeros((N, C, H_prime, W_prime))
  for i in range(H_prime):
    for j in range(W_prime):
      hs, he = i*pool_s, i*pool_s+pool_h
      ws, we = j*pool_s, j*pool_s+pool_w
      for n in range(N):
        for c in range(C):
          loc_max = np.max(x[n, c, hs:he, ws:we])
          out[n, c, i, j] = loc_max

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, pool_param)
  return out, cache


def max_pool_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a max pooling layer.

  Inputs:
  - dout: Upstream derivatives
  - cache: A tuple of (x, pool_param) as in the forward pass.

  Returns:
  - dx: Gradient with respect to x
  """
  #############################################################################
  # TODO: Implement the max pooling backward pass                             #
  #############################################################################
  (x, pool_param) = cache
  (N, C, H, W) = x.shape
  pool_h = pool_param['pool_height']
  pool_w = pool_param['pool_width']
  pool_s = pool_param['stride']

  H_prime = 1 + (H - pool_h) / pool_s
  W_prime = 1 + (W - pool_w) / pool_s

  dx = np.zeros(x.shape)
  for n in range(N):
    for c in range(C):
      for i in range(H_prime):
        for j in range(W_prime):
          hs, he = i*pool_s, i*pool_s+pool_h
          ws, we = j*pool_s, j*pool_s+pool_w
          local = x[n, c, hs:he, ws:we]
          max_idx = np.unravel_index(local.argmax(), local.shape)
          x_mask = np.zeros_like(local)
          x_mask[max_idx] += 1.
          dx[n, c, hs:he, ws:we] += dout[n, c, i, j] * x_mask
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
  """
  Computes the forward pass for spatial batch normalization.
  
  Inputs:
  - x: Input data of shape (N, C, H, W)
  - gamma: Scale parameter, of shape (C,)
  - beta: Shift parameter, of shape (C,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance. momentum=0 means that
      old information is discarded completely at every time step, while
      momentum=1 means that new information is never incorporated. The
      default of momentum=0.9 should work well in most situations.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features
    
  Returns a tuple of:
  - out: Output data, of shape (N, C, H, W)
  - cache: Values needed for the backward pass
  """
  out, cache = None, None

  #############################################################################
  # TODO: Implement the forward pass for spatial batch normalization.         #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  pass
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return out, cache


def spatial_batchnorm_backward(dout, cache):
  """
  Computes the backward pass for spatial batch normalization.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, C, H, W)
  - cache: Values from the forward pass
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs, of shape (N, C, H, W)
  - dgamma: Gradient with respect to scale parameter, of shape (C,)
  - dbeta: Gradient with respect to shift parameter, of shape (C,)
  """
  dx, dgamma, dbeta = None, None, None

  #############################################################################
  # TODO: Implement the backward pass for spatial batch normalization.        #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  pass
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta
  

def svm_loss(x, y, eps=1e-3):
  """
  Computes the loss and gradient using for multiclass SVM classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  N = x.shape[0]
  correct_class_scores = x[np.arange(N), y]
  margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
  margins[np.arange(N), y] = 0
  loss = np.sum(margins) / float(N + eps)
  num_pos = np.sum(margins > 0, axis=1)
  dx = np.zeros_like(x)
  dx[margins > 0] = 1
  dx[np.arange(N), y] -= num_pos
  dx /= float(N + eps)
  return loss, dx


def softmax_loss(x, y, eps=1e-8):
  """
  Computes the loss and gradient for softmax classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  probs = np.exp(x - np.max(x, axis=1, keepdims=True))
  probs /= np.sum(probs, axis=1, keepdims=True)
  probs += eps
  N = x.shape[0]
  loss = -np.sum(np.log(probs[np.arange(N), y])) / float(N + eps)
  dx = probs.copy()
  dx[np.arange(N), y] -= 1
  dx /= float(N + eps)
  return loss, dx
