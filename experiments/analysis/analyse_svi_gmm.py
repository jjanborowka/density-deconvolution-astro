import argparse
import collections
import os

import numpy as np
import torch
import torch.utils.data as data_utils

import pandas as pd

from deconv.gmm.sgd_deconv_gmm import SGDDeconvGMM
from deconv.gmm.sgd_gmm import SGDGMM
from deconv.gmm.data import DeconvDataset
from deconv.flow.svi_gmm import SVIGMMFlow
from deconv.utils.data_gen import generate_mixture_data

parser = argparse.ArgumentParser(description='Process SVI on GMM results.')

parser.add_argument('elbo_results_dir')

args = parser.parse_args()

K = 3
D = 2
N = 50000

_, S, _, _, (z_test, x_test) = generate_mixture_data()

elbo_params = []
for f in os.listdir(args.elbo_results_dir):
    path = os.path.join(args.elbo_results_dir, f)
    elbo_params.append(path)

test_gmm = SGDGMM(
    K,
    D,
    batch_size=200,
    device=torch.device('cuda'),
    w=0
)
test_deconv_gmm = SGDDeconvGMM(
    K,
    D,
    batch_size=512,
    device=torch.device('cuda'),
    w=0
)

svi_gmm = SVIGMMFlow(
    2,
    5,
    device=torch.device('cuda'),
    batch_size=512,
    epochs=100,
    lr=1e-4,
    n_samples=50,
    use_iwae=False,
    context_size=64,
    hidden_features=128
)

results = []

test_data = DeconvDataset(x_test.squeeze(), torch.linalg.cholesky(S.repeat(N, 1, 1)))
test_data_gmm = DeconvDataset(x_test.squeeze(), S.repeat(N, 1, 1))

torch.set_default_tensor_type(torch.cuda.FloatTensor)

for p in elbo_params:
    svi_gmm.model.load_state_dict(torch.load(p))
    test_gmm.module.load_state_dict(svi_gmm.model._prior.state_dict())
    with torch.no_grad():
        logv = test_gmm.module([z_test[0].to(torch.device('cuda'))]).mean().item()
    elbo = svi_gmm.score_batch(test_data, num_samples=500) / N
    logp = svi_gmm.score_batch(test_data, num_samples=500, log_prob=True) / N
    test_deconv_gmm.module.load_state_dict(svi_gmm.model._prior.state_dict())
    exact_log_p = test_deconv_gmm.score_batch(test_data_gmm) / N
    results.append({
            'i': 0,
            'model': 'svi_gmm',
            'elbo': elbo,
            'log_p_v': logv,
            'log_p_w': logp,
            'exact_log_p_w': exact_log_p,
            'kl': logp - elbo
    })

df = pd.DataFrame(results)
        
        
    
    