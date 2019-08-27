import numpy as np
import torch

import matplotlib.pyplot as plt
import seaborn as sns

from deconv.gmm.plotting import plot_covariance
from deconv.gmm.online_deconv_gmm import OnlineDeconvGMM
from deconv.gmm.sgd_deconv_gmm import SGDDeconvDataset

from data import generate_data


def check_online_deconv_gmm(D, K, N, plot=False, device=None, verbose=False):

    if not device:
        device = torch.device('cpu')

    data, params = generate_data(D, K, N)
    X_train, nc_train, X_test, nc_test = data
    means, covars = params

    train_data = SGDDeconvDataset(
        torch.Tensor(X_train.reshape(-1, D).astype(np.float32)),
        torch.Tensor(
            nc_train.reshape(-1, D, D).astype(np.float32)
        )
    )

    test_data = SGDDeconvDataset(
        torch.Tensor(X_test.reshape(-1, D).astype(np.float32)),
        torch.Tensor(
            nc_test.reshape(-1, D, D).astype(np.float32)
        )
    )

    gmm = OnlineDeconvGMM(
        K,
        D,
        device=device,
        batch_size=250,
        step_size=1e-2,
        restarts=5,
        w=1e-3
    )
    gmm.fit(train_data, val_data=test_data, verbose=verbose)

    train_score = gmm.score_batch(train_data)
    test_score = gmm.score_batch(test_data)

    print('Training score: {}'.format(train_score))
    print('Test score: {}'.format(test_score))

    if plot:
        fig, ax = plt.subplots()

        for i in range(K):
            sc = ax.scatter(
                X_train[:, i, 0],
                X_train[:, i, 1],
                alpha=0.2,
                marker='x',
                label='Cluster {}'.format(i)
            )
            plot_covariance(
                means[i, :],
                covars[i, :, :],
                ax,
                color=sc.get_facecolor()[0]
            )

        sc = ax.scatter(
            gmm.means[:, 0],
            gmm.means[:, 1],
            marker='+',
            label='Fitted Gaussians'
        )

        for i in range(K):
            plot_covariance(
                gmm.means[i, :],
                gmm.covars[i, :, :],
                ax,
                color=sc.get_facecolor()[0]
            )

        ax.legend()
        plt.show()


if __name__ == '__main__':
    sns.set()
    D = 2
    K = 3
    N = 500
    check_online_deconv_gmm(D, K, N, plot=True, verbose=True)
