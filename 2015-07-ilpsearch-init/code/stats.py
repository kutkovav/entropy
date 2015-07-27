__author__ = 'Jakub Danek'

import numpy as npy


"""
Given array of numbers, returns (mean_value, std_deviation) tuples.
"""
def makeStats(arr):
    avg = npy.mean(arr)
    std = npy.std(arr)

    return (avg, std)