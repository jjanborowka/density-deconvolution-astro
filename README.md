# Density Deconvolution with Normalizing Flows

This repository contains code for the experiments in our Density Deconvolution with Normalizing Flows adapted to astronomical data sets. 

## Setup

The `deconv` package can be installed using `pip install .`, or with `pip install -e .` if you wish to modify it.

For now you will need to use [our fork](https://github.com/JamesRitchie/nflows) of the `nflows` package until we can merge our changes upstream.

## Experiments

Experiments used in the paper are available under [experiments/flows](experiments/flows).


## TODO
1. Get this code up & running
  1. Run test cases
  2. Create jupyter notebooks with different 2D data sets
    1. Two moons
    2. Multiple donuts
3. Test how uncertainties need to be processed, answer following questions:
  1. What are the data point specific uncertainties that `nflows` processes?
  2. How can the Gaia specific uncertainty matrices be included into `nflows`?
  3. Do we trust the output?
