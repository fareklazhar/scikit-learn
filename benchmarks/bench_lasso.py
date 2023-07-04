"""
Benchmarks of Lasso vs LassoLars

First, we fix a training set and increase the number of
samples. Then we plot the computation time as function of
the number of samples.

In the second benchmark, we increase the number of dimensions of the
training set. Then we plot the computation time as function of
the number of dimensions.

In both cases, only 10% of the features are informative.
"""
import gc
from time import time
import numpy as np

from sklearn.datasets.samples_generator import make_regression


def compute_bench(alpha, n_samples, n_features, precompute):
    lars_lasso_results = []

    it = 0

    lasso_results = []
    for ns in n_samples:
        for nf in n_features:
            it += 1
            print('==================')
            print(f'Iteration {it} of {max(len(n_samples), len(n_features))}')
            print('==================')
            n_informative = nf // 10
            X, Y, coef_ = make_regression(n_samples=ns, n_features=nf,
                                          n_informative=n_informative,
                                          noise=0.1, coef=True)

            X /= np.sqrt(np.sum(X ** 2, axis=0))  # Normalize data

            gc.collect()
            print("- benchmarking Lasso")
            clf = Lasso(alpha=alpha, fit_intercept=False,
                        precompute=precompute)
            tstart = time()
            clf.fit(X, Y)
            lasso_results.append(time() - tstart)

            gc.collect()
            print("- benchmarking LassoLars")
            clf = LassoLars(alpha=alpha, fit_intercept=False,
                            normalize=False, precompute=precompute)
            tstart = time()
            clf.fit(X, Y)
            lars_lasso_results.append(time() - tstart)

    return lasso_results, lars_lasso_results


if __name__ == '__main__':
    from sklearn.linear_model import Lasso, LassoLars
    import pylab as pl

    alpha = 0.01  # regularization parameter

    n_features = 10
    list_n_samples = np.linspace(100, 1000000, 5).astype(np.int)
    lasso_results, lars_lasso_results = compute_bench(alpha, list_n_samples,
                                            [n_features], precompute=True)

    pl.figure('scikit-learn LASSO benchmark results')
    pl.subplot(211)
    pl.plot(list_n_samples, lasso_results, 'b-',
                            label='Lasso')
    pl.plot(list_n_samples, lars_lasso_results, 'r-',
                            label='LassoLars')
    pl.title('precomputed Gram matrix, %d features, alpha=%s' % (n_features, alpha))
    pl.legend(loc='upper left')
    pl.xlabel('number of samples')
    pl.ylabel('Time (s)')
    pl.axis('tight')

    n_samples = 2000
    list_n_features = np.linspace(500, 3000, 5).astype(np.int)
    lasso_results, lars_lasso_results = compute_bench(alpha, [n_samples],
                                           list_n_features, precompute=False)
    pl.subplot(212)
    pl.plot(list_n_features, lasso_results, 'b-', label='Lasso')
    pl.plot(list_n_features, lars_lasso_results, 'r-', label='LassoLars')
    pl.title('%d samples, alpha=%s' % (n_samples, alpha))
    pl.legend(loc='upper left')
    pl.xlabel('number of features')
    pl.ylabel('Time (s)')
    pl.axis('tight')
    pl.show()
