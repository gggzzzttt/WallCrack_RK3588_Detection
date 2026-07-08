#!/usr/bin/python
# -*- encoding: utf-8 -*-


import lib.data.transform_cv2 as T
from lib.data.base_dataset import BaseDataset
import cv2
import numpy as np


class CustomerDataset(BaseDataset):

    def __init__(self, dataroot, annpath, trans_func=None, mode='train'):
        super(CustomerDataset, self).__init__(
                dataroot, annpath, trans_func, mode)
        self.lb_ignore = 255

        self.to_tensor = T.ToTensor(
            mean=(0.4, 0.4, 0.4), # rgb
            std=(0.2, 0.2, 0.2),
        )

    def get_image(self, impth, lbpth):
        """读取图像和掩码，并将灰度掩码二值化"""
        # 读取图像 (BGR -> RGB)
        img = cv2.imread(impth)[:, :, ::-1].copy()
        
        # 读取掩码 (灰度)
        label = cv2.imread(lbpth, cv2.IMREAD_GRAYSCALE)
        
        # 二值化: > 127 的像素为裂缝(类别1), 否则为背景(类别0)
        label = (label > 127).astype(np.uint8)
        
        return img, label


