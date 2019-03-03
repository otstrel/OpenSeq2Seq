# pylint: skip-file
from open_seq2seq.models import Image2Label
from open_seq2seq.encoders import ResNetEncoder
from open_seq2seq.decoders import FullyConnectedDecoder
from open_seq2seq.losses import CrossEntropyLoss
from open_seq2seq.data import ImagenetDataLayer
from open_seq2seq.optimizers.lr_policies import piecewise_constant,  poly_decay
from open_seq2seq.optimizers.novograd  import NovoGrad, NovoGrad2, NovoGradW

import tensorflow as tf

data_root =""
# data_root = "/raid/Imagenet/tf-imagenet/"
base_model = Image2Label

base_params = {
  "random_seed": 0,
  "use_horovod": True, # False, #
  "num_gpus": 1,
  "batch_size_per_gpu": 128,

  "num_epochs": 100,

  "dtype": "mixed",
  "loss_scaling": "Backoff",

  "save_summaries_steps": 2000,
  "print_loss_steps": 100,
  "print_samples_steps": 10000,
  "eval_steps": 5000,
  "save_checkpoint_steps": 5000,
  "logdir": "logs/rn50/nvgd2w_lr1.0_wd0.001",

  "optimizer": NovoGrad2,
  "optimizer_params": {
    "beta1": 0.95,
    "beta2": 0.98,
    "epsilon": 1e-08,
    "weight_decay": 0.001,
  },

  "lr_policy": poly_decay,
  "lr_policy_params": {
    "learning_rate": 1.0,
    "power": 2,
    # "warmup_steps": 200,
  },

  # "optimizer": "Momentum",
  # "optimizer_params": {
  #   "momentum": 0.95,
  # },
  # "lr_policy": piecewise_constant,
  # "lr_policy_params": {
  #   "learning_rate": 0.1,
  #   "boundaries": [30, 60, 80, 90],
  #   "decay_rates": [0.1, 0.01, 0.001, 1e-4],
  # },
  # "regularizer": tf.contrib.layers.l2_regularizer,
  # "regularizer_params": {
  #   'scale': 0.0001, # 0.0001,
  # },

  "initializer": tf.variance_scaling_initializer,

  "summaries": ['learning_rate', 'variables', 'gradients', 'larc_summaries',
                'variable_norm', 'gradient_norm', 'global_gradient_norm'],
  "encoder": ResNetEncoder,
  "encoder_params": {
    'resnet_size': 50,
    "regularize_bn": False,
  },
  "decoder": FullyConnectedDecoder,
  "decoder_params": {
    "output_dim": 1000,
  },
  "loss": CrossEntropyLoss,
  "data_layer": ImagenetDataLayer,
  "data_layer_params": {
    "data_dir": data_root+"data", # "data",
    "image_size": 224,
    "num_classes": 1000,
  },
}