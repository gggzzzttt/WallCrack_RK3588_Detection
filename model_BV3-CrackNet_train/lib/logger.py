#!/usr/bin/python
# -*- encoding: utf-8 -*-


import os.path as osp
import time
import logging

import torch.distributed as dist


def setup_logger(name, logpth):
    rank = dist.get_rank() if dist.is_initialized() else 0
    multi_gpu = dist.is_initialized() and dist.get_world_size() > 1
    rank_prefix = 'rank{} '.format(rank) if multi_gpu else ''
    FORMAT = '{}%(levelname)s %(filename)s(%(lineno)d): %(message)s'.format(rank_prefix)

    if multi_gpu:
        obj_list = ['{}-{}.log'.format(name, time.strftime('%Y-%m-%d-%H-%M-%S'))
                    if rank == 0 else None]
        dist.broadcast_object_list(obj_list, src=0)
        logfile = osp.join(logpth, obj_list[0])
    else:
        logfile = osp.join(logpth, '{}-{}.log'.format(name, time.strftime('%Y-%m-%d-%H-%M-%S')))

    if dist.is_initialized() and rank != 0:
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.WARNING)
        fh.setFormatter(logging.Formatter(FORMAT))
        logging.root.setLevel(logging.WARNING)
        logging.root.addHandler(fh)
        return

    try:
        logging.basicConfig(level=logging.INFO, format=FORMAT, filename=logfile, force=True)
    except Exception:
        for hl in logging.root.handlers: logging.root.removeHandler(hl)
        logging.basicConfig(level=logging.INFO, format=FORMAT, filename=logfile)
    logging.root.addHandler(logging.StreamHandler())


def log_msg(it, max_iter, lr, time_meter, loss_meter, loss_pre_meter,
        loss_aux_meters):
    t_intv, eta = time_meter.get()
    loss_avg, _ = loss_meter.get()
    loss_pre_avg, _ = loss_pre_meter.get()
    loss_aux_avg = ', '.join(['{}: {:.4f}'.format(el.name, el.get()[0]) for el in loss_aux_meters])
    msg = ', '.join([
        f'iter: {it+1}/{max_iter}',
        f'lr: {lr:4f}',
        f'eta: {eta}',
        f'time: {t_intv:.2f}',
        f'loss: {loss_avg:.4f}',
        f'loss_pre: {loss_pre_avg:.4f}',
    ])
    msg += ', ' + loss_aux_avg

    return msg
