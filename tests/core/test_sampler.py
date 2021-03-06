import random
import unittest

import torch

from fastNLP import DataSet
from fastNLP import SequentialSampler, RandomSampler, BucketSampler
from fastNLP.core.sampler import k_means_1d, k_means_bucketing, simple_sort_bucketing


class TestSampler(unittest.TestCase):
    def test_sequential_sampler(self):
        sampler = SequentialSampler()
        data = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]
        for idx, i in enumerate(sampler(data)):
            assert idx == i

    def test_random_sampler(self):
        sampler = RandomSampler()
        data = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]
        ans = [data[i] for i in sampler(data)]
        assert len(ans) == len(data)
        for d in ans:
            assert d in data

    def test_k_means(self):
        centroids, assign = k_means_1d([21, 3, 25, 7, 9, 22, 4, 6, 28, 10], 2, max_iter=5)
        centroids, assign = list(centroids), list(assign)
        assert len(centroids) == 2
        assert len(assign) == 10

    def test_k_means_bucketing(self):
        res = k_means_bucketing([21, 3, 25, 7, 9, 22, 4, 6, 28, 10], [None, None])
        assert len(res) == 2

    def test_simple_sort_bucketing(self):
        _ = simple_sort_bucketing([21, 3, 25, 7, 9, 22, 4, 6, 28, 10])
        assert len(_) == 10

    def test_BucketSampler(self):
        sampler = BucketSampler(num_buckets=3, batch_size=16, seq_len_field_name="seq_len")
        data_set = DataSet({"x": [[0] * random.randint(1, 10)] * 10, "y": [[5, 6]] * 10})
        data_set.apply(lambda ins: len(ins["x"]), new_field_name="seq_len")
        indices = sampler(data_set)
        self.assertEqual(len(indices), 10)
        # 跑通即可，不验证效果

    def test_ConstantTokenNumSampler(self):
        # 需要check的是，是否在number上是接近的
        pass

    def test_ConstTokenNumSampler(self):
        # 需要check的是，是否可以直接运行
        pass
