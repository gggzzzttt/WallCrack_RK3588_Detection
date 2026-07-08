D:\conda_envs\yolov10\python.exe D:\coding\BiSeNet-master\crack_classifier\train.py
2026-06-18 16:19:54.041494: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:19:54.041606: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
保存目录: ./res/crack_classifier\mobilenetv3_small
TensorBoard 日志: ./res/crack_classifier\mobilenetv3_small\tensorboard\20260618_161956
模型总参数量: 1.67M
可训练参数量: 1.67M
输入通道数: 4
分类数: 5
加载数据集...
[train] 加载数据: 7325 张
[val] 加载数据: 914 张
[test] 加载数据: 920 张

============================================================
开始训练
============================================================
设备: cuda
总 epochs: 100
Batch size: 32
使用掩码: True
============================================================

2026-06-18 16:19:58.450073: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:19:58.450183: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:20:02.396642: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:20:02.396746: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:20:06.352543: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:20:06.352650: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:20:10.307521: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:20:10.307647: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [1/100] [50/228] Loss: 1.3597 Acc: 0.4213 LR: 0.000500
Epoch [1/100] [100/228] Loss: 1.2741 Acc: 0.4938 LR: 0.000500
Epoch [1/100] [150/228] Loss: 1.2370 Acc: 0.5229 LR: 0.000500
Epoch [1/100] [200/228] Loss: 1.2090 Acc: 0.5433 LR: 0.000500
2026-06-18 16:20:26.949466: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:20:26.949575: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:20:30.940893: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:20:30.940998: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:20:34.870258: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:20:34.870364: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:20:38.862809: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:20:38.862921: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.5460
  类别 0 (无裂缝): 0.9787 (138/141)
  类别 1 (轻度裂缝): 0.5591 (123/220)
  类别 2 (中度裂缝): 0.5993 (175/292)
  类别 3 (重度裂缝): 0.1429 (24/168)
  类别 4 (严重裂缝): 0.4194 (39/93)

Epoch [1/100] 总结:
  Train Loss: 1.1971, Train Acc: 0.5526
  Val Loss: 1.2944, Val Acc: 0.5460
  LR: 0.000500


保存最佳模型: ./res/crack_classifier\mobilenetv3_small\model_best.pth (Acc: 0.5460)
2026-06-18 16:20:45.081139: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:20:45.081245: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:20:49.247965: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:20:49.248071: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:20:53.205559: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:20:53.205661: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:20:57.123148: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:20:57.123358: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [2/100] [50/228] Loss: 1.0570 Acc: 0.6619 LR: 0.000500
Epoch [2/100] [100/228] Loss: 1.0495 Acc: 0.6644 LR: 0.000500
Epoch [2/100] [150/228] Loss: 1.0400 Acc: 0.6667 LR: 0.000500
Epoch [2/100] [200/228] Loss: 1.0285 Acc: 0.6731 LR: 0.000500
2026-06-18 16:21:13.553150: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:21:13.553255: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:21:17.510086: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:21:17.510190: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:21:21.431662: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:21:21.431772: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:21:25.356810: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:21:25.356933: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.6204
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.4455 (98/220)
  类别 2 (中度裂缝): 0.6986 (204/292)
  类别 3 (重度裂缝): 0.4881 (82/168)
  类别 4 (严重裂缝): 0.4516 (42/93)

Epoch [2/100] 总结:
  Train Loss: 1.0271, Train Acc: 0.6734
  Val Loss: 1.1539, Val Acc: 0.6204
  LR: 0.000500


保存最佳模型: ./res/crack_classifier\mobilenetv3_small\model_best.pth (Acc: 0.6204)
2026-06-18 16:21:31.324889: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:21:31.325002: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:21:35.280516: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:21:35.280630: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:21:39.241799: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:21:39.241923: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:21:43.174420: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:21:43.174524: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [3/100] [50/228] Loss: 0.9501 Acc: 0.7231 LR: 0.000500
Epoch [3/100] [100/228] Loss: 0.9368 Acc: 0.7325 LR: 0.000500
Epoch [3/100] [150/228] Loss: 0.9314 Acc: 0.7312 LR: 0.000500
Epoch [3/100] [200/228] Loss: 0.9260 Acc: 0.7334 LR: 0.000500
2026-06-18 16:21:59.228055: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:21:59.228164: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:22:03.174809: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:22:03.174916: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:22:07.249901: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:22:07.250014: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:22:11.200097: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:22:11.200201: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.6586
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.5682 (125/220)
  类别 2 (中度裂缝): 0.8664 (253/292)
  类别 3 (重度裂缝): 0.3095 (52/168)
  类别 4 (严重裂缝): 0.3333 (31/93)

Epoch [3/100] 总结:
  Train Loss: 0.9210, Train Acc: 0.7368
  Val Loss: 1.1704, Val Acc: 0.6586
  LR: 0.000499


保存最佳模型: ./res/crack_classifier\mobilenetv3_small\model_best.pth (Acc: 0.6586)
2026-06-18 16:22:17.210543: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:22:17.210647: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:22:21.154803: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:22:21.154990: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:22:25.119717: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:22:25.119820: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:22:29.081837: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:22:29.081942: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [4/100] [50/228] Loss: 0.8668 Acc: 0.7600 LR: 0.000499
Epoch [4/100] [100/228] Loss: 0.8697 Acc: 0.7612 LR: 0.000499
Epoch [4/100] [150/228] Loss: 0.8608 Acc: 0.7633 LR: 0.000499
Epoch [4/100] [200/228] Loss: 0.8550 Acc: 0.7655 LR: 0.000499
2026-06-18 16:22:45.160543: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:22:45.160651: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:22:49.095077: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:22:49.095186: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:22:53.011798: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:22:53.011908: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:22:56.986161: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:22:56.986286: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7615
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8182 (180/220)
  类别 2 (中度裂缝): 0.7671 (224/292)
  类别 3 (重度裂缝): 0.5417 (91/168)
  类别 4 (严重裂缝): 0.6452 (60/93)

Epoch [4/100] 总结:
  Train Loss: 0.8525, Train Acc: 0.7666
  Val Loss: 0.9509, Val Acc: 0.7615
  LR: 0.000498


保存最佳模型: ./res/crack_classifier\mobilenetv3_small\model_best.pth (Acc: 0.7615)
2026-06-18 16:23:02.969159: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:23:02.969267: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:23:06.917777: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:23:06.917886: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:23:10.872099: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:23:10.872205: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:23:14.815580: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:23:14.815687: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [5/100] [50/228] Loss: 0.8300 Acc: 0.7863 LR: 0.000498
Epoch [5/100] [100/228] Loss: 0.8287 Acc: 0.7856 LR: 0.000498
Epoch [5/100] [150/228] Loss: 0.8267 Acc: 0.7879 LR: 0.000498
Epoch [5/100] [200/228] Loss: 0.8234 Acc: 0.7900 LR: 0.000498
2026-06-18 16:23:30.838246: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:23:30.838352: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:23:34.783486: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:23:34.783591: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:23:38.710901: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:23:38.711008: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:23:42.645422: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:23:42.645530: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7768
  类别 0 (无裂缝): 0.9929 (140/141)
  类别 1 (轻度裂缝): 0.8091 (178/220)
  类别 2 (中度裂缝): 0.7740 (226/292)
  类别 3 (重度裂缝): 0.6667 (112/168)
  类别 4 (严重裂缝): 0.5806 (54/93)

Epoch [5/100] 总结:
  Train Loss: 0.8225, Train Acc: 0.7907
  Val Loss: 0.8692, Val Acc: 0.7768
  LR: 0.000497


保存最佳模型: ./res/crack_classifier\mobilenetv3_small\model_best.pth (Acc: 0.7768)
2026-06-18 16:23:48.606584: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:23:48.606691: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:23:52.522693: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:23:52.522798: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:23:56.454095: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:23:56.454208: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:24:00.411157: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:24:00.411262: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [6/100] [50/228] Loss: 0.7932 Acc: 0.8081 LR: 0.000497
Epoch [6/100] [100/228] Loss: 0.7871 Acc: 0.8078 LR: 0.000497
Epoch [6/100] [150/228] Loss: 0.7815 Acc: 0.8110 LR: 0.000497
Epoch [6/100] [200/228] Loss: 0.7813 Acc: 0.8123 LR: 0.000497
2026-06-18 16:24:16.513055: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:24:16.513160: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:24:20.435876: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:24:20.435988: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:24:24.392671: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:24:24.392774: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:24:28.372134: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:24:28.372241: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7823
  类别 0 (无裂缝): 0.9858 (139/141)
  类别 1 (轻度裂缝): 0.8636 (190/220)
  类别 2 (中度裂缝): 0.6610 (193/292)
  类别 3 (重度裂缝): 0.7083 (119/168)
  类别 4 (严重裂缝): 0.7957 (74/93)

Epoch [6/100] 总结:
  Train Loss: 0.7886, Train Acc: 0.8074
  Val Loss: 0.8494, Val Acc: 0.7823
  LR: 0.000496


保存最佳模型: ./res/crack_classifier\mobilenetv3_small\model_best.pth (Acc: 0.7823)
2026-06-18 16:24:34.324597: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:24:34.324706: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:24:38.283771: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:24:38.283917: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:24:42.234073: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:24:42.234182: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:24:46.176470: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:24:46.176573: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [7/100] [50/228] Loss: 0.7841 Acc: 0.7981 LR: 0.000496
Epoch [7/100] [100/228] Loss: 0.7694 Acc: 0.8113 LR: 0.000496
Epoch [7/100] [150/228] Loss: 0.7773 Acc: 0.8067 LR: 0.000496
Epoch [7/100] [200/228] Loss: 0.7745 Acc: 0.8091 LR: 0.000496
2026-06-18 16:25:02.153770: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:25:02.153876: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:25:06.117617: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:25:06.117723: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:25:10.065221: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:25:10.065339: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:25:14.002993: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:25:14.003198: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7932
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8227 (181/220)
  类别 2 (中度裂缝): 0.7192 (210/292)
  类别 3 (重度裂缝): 0.8333 (140/168)
  类别 4 (严重裂缝): 0.5699 (53/93)

Epoch [7/100] 总结:
  Train Loss: 0.7778, Train Acc: 0.8070
  Val Loss: 0.8400, Val Acc: 0.7932
  LR: 0.000494


保存最佳模型: ./res/crack_classifier\mobilenetv3_small\model_best.pth (Acc: 0.7932)
2026-06-18 16:25:19.980679: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:25:19.980791: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:25:23.985342: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:25:23.985448: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:25:27.951377: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:25:27.951484: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:25:31.919884: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:25:31.919994: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [8/100] [50/228] Loss: 0.7521 Acc: 0.8225 LR: 0.000494
Epoch [8/100] [100/228] Loss: 0.7616 Acc: 0.8178 LR: 0.000494
Epoch [8/100] [150/228] Loss: 0.7523 Acc: 0.8267 LR: 0.000494
Epoch [8/100] [200/228] Loss: 0.7550 Acc: 0.8264 LR: 0.000494
2026-06-18 16:25:48.367102: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:25:48.367200: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:25:52.449055: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:25:52.449161: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:25:56.848287: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:25:56.848398: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:26:01.183986: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:26:01.184091: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7593
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8227 (181/220)
  类别 2 (中度裂缝): 0.6233 (182/292)
  类别 3 (重度裂缝): 0.7560 (127/168)
  类别 4 (严重裂缝): 0.6774 (63/93)

Epoch [8/100] 总结:
  Train Loss: 0.7560, Train Acc: 0.8231
  Val Loss: 0.8908, Val Acc: 0.7593
  LR: 0.000492

2026-06-18 16:26:07.825398: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:26:07.825501: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:26:12.202825: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:26:12.202928: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:26:16.515669: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:26:16.515780: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:26:20.829335: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:26:20.829441: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [9/100] [50/228] Loss: 0.7353 Acc: 0.8431 LR: 0.000492
Epoch [9/100] [100/228] Loss: 0.7505 Acc: 0.8306 LR: 0.000492
Epoch [9/100] [150/228] Loss: 0.7543 Acc: 0.8281 LR: 0.000492
Epoch [9/100] [200/228] Loss: 0.7509 Acc: 0.8313 LR: 0.000492
2026-06-18 16:26:39.097751: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:26:39.097857: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:26:43.471480: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:26:43.471599: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:26:47.932015: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:26:47.932121: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:26:52.350486: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:26:52.350595: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8096
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.9091 (200/220)
  类别 2 (中度裂缝): 0.7192 (210/292)
  类别 3 (重度裂缝): 0.7262 (122/168)
  类别 4 (严重裂缝): 0.7204 (67/93)

Epoch [9/100] 总结:
  Train Loss: 0.7491, Train Acc: 0.8313
  Val Loss: 0.8063, Val Acc: 0.8096
  LR: 0.000490


保存最佳模型: ./res/crack_classifier\mobilenetv3_small\model_best.pth (Acc: 0.8096)
2026-06-18 16:26:59.130861: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:26:59.130969: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:27:03.486090: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:27:03.486191: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:27:07.841867: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:27:07.841969: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:27:12.170707: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:27:12.170817: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [10/100] [50/228] Loss: 0.7199 Acc: 0.8488 LR: 0.000490
Epoch [10/100] [100/228] Loss: 0.7319 Acc: 0.8422 LR: 0.000490
Epoch [10/100] [150/228] Loss: 0.7302 Acc: 0.8410 LR: 0.000490
Epoch [10/100] [200/228] Loss: 0.7373 Acc: 0.8370 LR: 0.000490
2026-06-18 16:27:30.647005: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:27:30.647113: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:27:34.929534: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:27:34.929646: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:27:39.233484: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:27:39.233595: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:27:43.583537: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:27:43.583647: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7867
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8818 (194/220)
  类别 2 (中度裂缝): 0.7021 (205/292)
  类别 3 (重度裂缝): 0.6548 (110/168)
  类别 4 (严重裂缝): 0.7419 (69/93)

Epoch [10/100] 总结:
  Train Loss: 0.7394, Train Acc: 0.8340
  Val Loss: 0.8518, Val Acc: 0.7867
  LR: 0.000488

2026-06-18 16:27:50.245453: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:27:50.245558: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:27:54.615858: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:27:54.615962: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:27:58.952131: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:27:58.952295: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:28:03.284083: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:28:03.284194: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [11/100] [50/228] Loss: 0.6976 Acc: 0.8594 LR: 0.000488
Epoch [11/100] [100/228] Loss: 0.7265 Acc: 0.8419 LR: 0.000488
Epoch [11/100] [150/228] Loss: 0.7344 Acc: 0.8352 LR: 0.000488
Epoch [11/100] [200/228] Loss: 0.7294 Acc: 0.8370 LR: 0.000488
2026-06-18 16:28:21.894755: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:28:21.894861: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:28:26.326491: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:28:26.326596: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:28:30.732013: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:28:30.732120: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:28:35.156798: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:28:35.156895: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7287
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.9136 (201/220)
  类别 2 (中度裂缝): 0.5719 (167/292)
  类别 3 (重度裂缝): 0.5298 (89/168)
  类别 4 (严重裂缝): 0.7312 (68/93)

Epoch [11/100] 总结:
  Train Loss: 0.7323, Train Acc: 0.8366
  Val Loss: 0.9343, Val Acc: 0.7287
  LR: 0.000485

2026-06-18 16:28:41.864903: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:28:41.865002: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:28:46.121001: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:28:46.121105: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:28:50.356181: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:28:50.356291: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:28:54.722786: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:28:54.722898: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [12/100] [50/228] Loss: 0.6928 Acc: 0.8550 LR: 0.000485
Epoch [12/100] [100/228] Loss: 0.7049 Acc: 0.8516 LR: 0.000485
Epoch [12/100] [150/228] Loss: 0.7146 Acc: 0.8419 LR: 0.000485
Epoch [12/100] [200/228] Loss: 0.7152 Acc: 0.8436 LR: 0.000485
2026-06-18 16:29:12.996579: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:29:12.996676: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:29:17.243703: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:29:17.243811: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:29:21.481206: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:29:21.481311: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:29:25.693602: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:29:25.693724: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7615
  类别 0 (无裂缝): 0.9929 (140/141)
  类别 1 (轻度裂缝): 0.9136 (201/220)
  类别 2 (中度裂缝): 0.5856 (171/292)
  类别 3 (重度裂缝): 0.7202 (121/168)
  类别 4 (严重裂缝): 0.6774 (63/93)

Epoch [12/100] 总结:
  Train Loss: 0.7181, Train Acc: 0.8414
  Val Loss: 0.8989, Val Acc: 0.7615
  LR: 0.000482

2026-06-18 16:29:32.169640: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:29:32.169751: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:29:36.436746: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:29:36.436854: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:29:40.638676: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:29:40.638778: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:29:44.976759: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:29:44.976865: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [13/100] [50/228] Loss: 0.6937 Acc: 0.8569 LR: 0.000482
Epoch [13/100] [100/228] Loss: 0.7091 Acc: 0.8541 LR: 0.000482
Epoch [13/100] [150/228] Loss: 0.7157 Acc: 0.8460 LR: 0.000482
Epoch [13/100] [200/228] Loss: 0.7060 Acc: 0.8527 LR: 0.000482
2026-06-18 16:30:02.990529: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:30:02.990632: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:30:07.273644: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:30:07.273747: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:30:11.513139: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:30:11.513267: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:30:15.742052: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:30:15.742158: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7779
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.9227 (203/220)
  类别 2 (中度裂缝): 0.6199 (181/292)
  类别 3 (重度裂缝): 0.6786 (114/168)
  类别 4 (严重裂缝): 0.7742 (72/93)

Epoch [13/100] 总结:
  Train Loss: 0.7088, Train Acc: 0.8521
  Val Loss: 0.8560, Val Acc: 0.7779
  LR: 0.000479

2026-06-18 16:30:22.338226: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:30:22.338338: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:30:26.721071: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:30:26.721177: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:30:31.105231: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:30:31.105335: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:30:35.432839: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:30:35.432948: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [14/100] [50/228] Loss: 0.7103 Acc: 0.8444 LR: 0.000479
Epoch [14/100] [100/228] Loss: 0.7001 Acc: 0.8503 LR: 0.000479
Epoch [14/100] [150/228] Loss: 0.7023 Acc: 0.8523 LR: 0.000479
Epoch [14/100] [200/228] Loss: 0.7026 Acc: 0.8539 LR: 0.000479
2026-06-18 16:30:53.813815: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:30:53.813921: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:30:58.171491: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:30:58.171594: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:31:02.488347: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:31:02.488451: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:31:06.770318: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:31:06.770428: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7845
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8909 (196/220)
  类别 2 (中度裂缝): 0.6575 (192/292)
  类别 3 (重度裂缝): 0.6905 (116/168)
  类别 4 (严重裂缝): 0.7742 (72/93)

Epoch [14/100] 总结:
  Train Loss: 0.7002, Train Acc: 0.8549
  Val Loss: 0.8527, Val Acc: 0.7845
  LR: 0.000476

2026-06-18 16:31:13.344964: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:31:13.345089: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:31:17.654915: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:31:17.655022: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:31:21.993566: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:31:21.993675: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:31:26.237214: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:31:26.237332: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [15/100] [50/228] Loss: 0.7179 Acc: 0.8363 LR: 0.000476
Epoch [15/100] [100/228] Loss: 0.7122 Acc: 0.8444 LR: 0.000476
Epoch [15/100] [150/228] Loss: 0.7061 Acc: 0.8496 LR: 0.000476
Epoch [15/100] [200/228] Loss: 0.6999 Acc: 0.8531 LR: 0.000476
2026-06-18 16:31:44.082163: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:31:44.082266: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:31:48.405444: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:31:48.405551: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:31:52.699353: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:31:52.699465: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:31:56.968953: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:31:56.969063: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7385
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8500 (187/220)
  类别 2 (中度裂缝): 0.5925 (173/292)
  类别 3 (重度裂缝): 0.7083 (119/168)
  类别 4 (严重裂缝): 0.5914 (55/93)

Epoch [15/100] 总结:
  Train Loss: 0.7018, Train Acc: 0.8520
  Val Loss: 0.9305, Val Acc: 0.7385
  LR: 0.000473

2026-06-18 16:32:03.561801: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:32:03.561908: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:32:07.836210: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:32:07.836318: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:32:12.122337: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:32:12.122448: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:32:16.432260: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:32:16.432392: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [16/100] [50/228] Loss: 0.6563 Acc: 0.8719 LR: 0.000473
Epoch [16/100] [100/228] Loss: 0.6710 Acc: 0.8659 LR: 0.000473
Epoch [16/100] [150/228] Loss: 0.6716 Acc: 0.8654 LR: 0.000473
Epoch [16/100] [200/228] Loss: 0.6768 Acc: 0.8627 LR: 0.000473
2026-06-18 16:32:34.768458: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:32:34.768563: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:32:39.148192: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:32:39.148297: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:32:43.501304: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:32:43.501408: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:32:47.803391: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:32:47.803502: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8053
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8591 (189/220)
  类别 2 (中度裂缝): 0.6781 (198/292)
  类别 3 (重度裂缝): 0.8393 (141/168)
  类别 4 (严重裂缝): 0.7204 (67/93)

Epoch [16/100] 总结:
  Train Loss: 0.6777, Train Acc: 0.8620
  Val Loss: 0.8036, Val Acc: 0.8053
  LR: 0.000469

2026-06-18 16:32:54.355189: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:32:54.355315: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:32:58.656041: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:32:58.656165: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:33:02.973884: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:33:02.973992: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:33:07.214034: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:33:07.214148: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [17/100] [50/228] Loss: 0.6618 Acc: 0.8800 LR: 0.000469
Epoch [17/100] [100/228] Loss: 0.6631 Acc: 0.8747 LR: 0.000469
Epoch [17/100] [150/228] Loss: 0.6666 Acc: 0.8735 LR: 0.000469
Epoch [17/100] [200/228] Loss: 0.6728 Acc: 0.8662 LR: 0.000469
2026-06-18 16:33:24.870788: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:33:24.870889: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:33:29.120058: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:33:29.120164: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:33:33.362150: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:33:33.362276: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:33:37.603354: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:33:37.603464: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7801
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8000 (176/220)
  类别 2 (中度裂缝): 0.6541 (191/292)
  类别 3 (重度裂缝): 0.8452 (142/168)
  类别 4 (严重裂缝): 0.6774 (63/93)

Epoch [17/100] 总结:
  Train Loss: 0.6782, Train Acc: 0.8644
  Val Loss: 0.8186, Val Acc: 0.7801
  LR: 0.000465

2026-06-18 16:33:44.093478: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:33:44.093577: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:33:48.356597: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:33:48.356709: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:33:52.610938: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:33:52.611046: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:33:56.897973: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:33:56.898087: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [18/100] [50/228] Loss: 0.6395 Acc: 0.8862 LR: 0.000465
Epoch [18/100] [100/228] Loss: 0.6562 Acc: 0.8806 LR: 0.000465
Epoch [18/100] [150/228] Loss: 0.6572 Acc: 0.8804 LR: 0.000465
Epoch [18/100] [200/228] Loss: 0.6621 Acc: 0.8770 LR: 0.000465
2026-06-18 16:34:14.304363: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:34:14.304508: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:34:18.583098: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:34:18.583209: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:34:22.806736: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:34:22.806848: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:34:27.038005: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:34:27.038111: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8337
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.9227 (203/220)
  类别 2 (中度裂缝): 0.7363 (215/292)
  类别 3 (重度裂缝): 0.7917 (133/168)
  类别 4 (严重裂缝): 0.7527 (70/93)

Epoch [18/100] 总结:
  Train Loss: 0.6656, Train Acc: 0.8753
  Val Loss: 0.7757, Val Acc: 0.8337
  LR: 0.000461


保存最佳模型: ./res/crack_classifier\mobilenetv3_small\model_best.pth (Acc: 0.8337)
2026-06-18 16:34:33.557844: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:34:33.557949: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:34:37.885584: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:34:37.885690: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:34:42.195330: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:34:42.195451: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:34:46.608021: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:34:46.608136: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [19/100] [50/228] Loss: 0.6518 Acc: 0.8800 LR: 0.000461
Epoch [19/100] [100/228] Loss: 0.6576 Acc: 0.8744 LR: 0.000461
Epoch [19/100] [150/228] Loss: 0.6609 Acc: 0.8725 LR: 0.000461
Epoch [19/100] [200/228] Loss: 0.6624 Acc: 0.8723 LR: 0.000461
2026-06-18 16:35:03.778298: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:35:03.778401: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:35:08.084826: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:35:08.084926: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:35:12.415702: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:35:12.415805: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:35:16.765176: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:35:16.765288: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7812
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8955 (197/220)
  类别 2 (中度裂缝): 0.6370 (186/292)
  类别 3 (重度裂缝): 0.6667 (112/168)
  类别 4 (严重裂缝): 0.8387 (78/93)

Epoch [19/100] 总结:
  Train Loss: 0.6640, Train Acc: 0.8701
  Val Loss: 0.8652, Val Acc: 0.7812
  LR: 0.000457

2026-06-18 16:35:23.161241: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:35:23.161348: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:35:27.428781: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:35:27.428878: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:35:31.707792: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:35:31.707893: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:35:35.992886: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:35:35.992996: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [20/100] [50/228] Loss: 0.6542 Acc: 0.8706 LR: 0.000457
Epoch [20/100] [100/228] Loss: 0.6427 Acc: 0.8803 LR: 0.000457
Epoch [20/100] [150/228] Loss: 0.6429 Acc: 0.8802 LR: 0.000457
Epoch [20/100] [200/228] Loss: 0.6403 Acc: 0.8814 LR: 0.000457
2026-06-18 16:35:53.271297: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:35:53.271401: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:35:57.248415: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:35:57.248519: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:36:01.177425: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:36:01.177534: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:36:05.141286: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:36:05.141392: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8020
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8182 (180/220)
  类别 2 (中度裂缝): 0.7397 (216/292)
  类别 3 (重度裂缝): 0.7679 (129/168)
  类别 4 (严重裂缝): 0.7204 (67/93)

Epoch [20/100] 总结:
  Train Loss: 0.6438, Train Acc: 0.8812
  Val Loss: 0.8075, Val Acc: 0.8020
  LR: 0.000452

2026-06-18 16:36:11.115441: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:36:11.115542: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:36:15.064348: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:36:15.064456: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:36:19.073202: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:36:19.073303: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:36:23.063440: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:36:23.063539: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [21/100] [50/228] Loss: 0.6101 Acc: 0.8962 LR: 0.000452
Epoch [21/100] [100/228] Loss: 0.6273 Acc: 0.8947 LR: 0.000452
Epoch [21/100] [150/228] Loss: 0.6359 Acc: 0.8860 LR: 0.000452
Epoch [21/100] [200/228] Loss: 0.6366 Acc: 0.8855 LR: 0.000452
2026-06-18 16:36:39.311196: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:36:39.311303: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:36:43.667489: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:36:43.667624: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:36:48.129826: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:36:48.129941: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:36:52.511562: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:36:52.511717: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8118
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.9136 (201/220)
  类别 2 (中度裂缝): 0.7192 (210/292)
  类别 3 (重度裂缝): 0.7262 (122/168)
  类别 4 (严重裂缝): 0.7312 (68/93)

Epoch [21/100] 总结:
  Train Loss: 0.6368, Train Acc: 0.8846
  Val Loss: 0.8509, Val Acc: 0.8118
  LR: 0.000448

2026-06-18 16:36:59.369488: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:36:59.369601: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:37:03.856907: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:37:03.857013: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:37:08.311106: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:37:08.311207: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:37:12.746642: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:37:12.746754: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [22/100] [50/228] Loss: 0.6040 Acc: 0.8969 LR: 0.000448
Epoch [22/100] [100/228] Loss: 0.6153 Acc: 0.8981 LR: 0.000448
Epoch [22/100] [150/228] Loss: 0.6172 Acc: 0.8950 LR: 0.000448
Epoch [22/100] [200/228] Loss: 0.6182 Acc: 0.8938 LR: 0.000448
2026-06-18 16:37:31.258057: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:37:31.258170: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:37:35.539639: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:37:35.539743: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:37:39.811439: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:37:39.811556: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:37:44.107179: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:37:44.107290: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7965
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.9318 (205/220)
  类别 2 (中度裂缝): 0.6986 (204/292)
  类别 3 (重度裂缝): 0.7798 (131/168)
  类别 4 (严重裂缝): 0.5054 (47/93)

Epoch [22/100] 总结:
  Train Loss: 0.6270, Train Acc: 0.8895
  Val Loss: 0.8537, Val Acc: 0.7965
  LR: 0.000443

2026-06-18 16:37:50.663419: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:37:50.663524: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:37:54.989677: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:37:54.989782: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:37:59.255510: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:37:59.255631: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:38:03.553614: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:38:03.553725: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [23/100] [50/228] Loss: 0.5935 Acc: 0.9069 LR: 0.000443
Epoch [23/100] [100/228] Loss: 0.5986 Acc: 0.9047 LR: 0.000443
Epoch [23/100] [150/228] Loss: 0.6091 Acc: 0.9004 LR: 0.000443
Epoch [23/100] [200/228] Loss: 0.6180 Acc: 0.8970 LR: 0.000443
2026-06-18 16:38:21.825691: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:38:21.825805: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:38:26.118693: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:38:26.118800: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:38:30.421636: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:38:30.421737: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:38:34.688979: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:38:34.689103: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8162
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8773 (193/220)
  类别 2 (中度裂缝): 0.7466 (218/292)
  类别 3 (重度裂缝): 0.7857 (132/168)
  类别 4 (严重裂缝): 0.6667 (62/93)

Epoch [23/100] 总结:
  Train Loss: 0.6223, Train Acc: 0.8969
  Val Loss: 0.8286, Val Acc: 0.8162
  LR: 0.000438

2026-06-18 16:38:41.143786: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:38:41.143893: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:38:45.451652: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:38:45.451761: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:38:49.737457: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:38:49.737560: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:38:54.117449: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:38:54.117570: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [24/100] [50/228] Loss: 0.5945 Acc: 0.9044 LR: 0.000438
Epoch [24/100] [100/228] Loss: 0.6028 Acc: 0.9022 LR: 0.000438
Epoch [24/100] [150/228] Loss: 0.6102 Acc: 0.8979 LR: 0.000438
Epoch [24/100] [200/228] Loss: 0.6060 Acc: 0.9009 LR: 0.000438
2026-06-18 16:39:12.361380: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:39:12.361485: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:39:16.639545: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:39:16.639648: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:39:20.644168: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:39:20.644275: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:39:24.682244: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:39:24.682402: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8184
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.7545 (166/220)
  类别 2 (中度裂缝): 0.8356 (244/292)
  类别 3 (重度裂缝): 0.6964 (117/168)
  类别 4 (严重裂缝): 0.8602 (80/93)

Epoch [24/100] 总结:
  Train Loss: 0.6127, Train Acc: 0.8978
  Val Loss: 0.8057, Val Acc: 0.8184
  LR: 0.000432

2026-06-18 16:39:30.806362: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:39:30.806478: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:39:34.869255: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:39:34.869360: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:39:38.868543: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:39:38.868647: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:39:42.884783: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:39:42.884888: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [25/100] [50/228] Loss: 0.6077 Acc: 0.8988 LR: 0.000432
Epoch [25/100] [100/228] Loss: 0.6058 Acc: 0.8988 LR: 0.000432
Epoch [25/100] [150/228] Loss: 0.6049 Acc: 0.9021 LR: 0.000432
Epoch [25/100] [200/228] Loss: 0.6054 Acc: 0.9016 LR: 0.000432
2026-06-18 16:40:01.090880: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:40:01.090993: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:40:05.366765: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:40:05.366877: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:40:09.659670: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:40:09.659782: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:40:14.023307: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:40:14.023409: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8140
  类别 0 (无裂缝): 0.9929 (140/141)
  类别 1 (轻度裂缝): 0.7909 (174/220)
  类别 2 (中度裂缝): 0.8253 (241/292)
  类别 3 (重度裂缝): 0.6845 (115/168)
  类别 4 (严重裂缝): 0.7957 (74/93)

Epoch [25/100] 总结:
  Train Loss: 0.6021, Train Acc: 0.9025
  Val Loss: 0.8091, Val Acc: 0.8140
  LR: 0.000427

2026-06-18 16:40:20.671011: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:40:20.671111: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:40:24.952701: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:40:24.952804: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:40:29.264862: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:40:29.264966: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:40:33.553953: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:40:33.554115: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [26/100] [50/228] Loss: 0.5554 Acc: 0.9313 LR: 0.000427
Epoch [26/100] [100/228] Loss: 0.5732 Acc: 0.9200 LR: 0.000427
Epoch [26/100] [150/228] Loss: 0.5837 Acc: 0.9131 LR: 0.000427
Epoch [26/100] [200/228] Loss: 0.5886 Acc: 0.9125 LR: 0.000427
2026-06-18 16:40:51.166331: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:40:51.166435: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:40:55.517000: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:40:55.517099: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:40:59.635788: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:40:59.635885: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:41:03.743046: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:41:03.743156: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7976
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8864 (195/220)
  类别 2 (中度裂缝): 0.7568 (221/292)
  类别 3 (重度裂缝): 0.6786 (114/168)
  类别 4 (严重裂缝): 0.6237 (58/93)

Epoch [26/100] 总结:
  Train Loss: 0.5899, Train Acc: 0.9110
  Val Loss: 0.9048, Val Acc: 0.7976
  LR: 0.000421

2026-06-18 16:41:10.426277: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:41:10.426376: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:41:14.706200: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:41:14.706301: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:41:18.761700: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:41:18.761796: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:41:22.719486: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:41:22.719602: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [27/100] [50/228] Loss: 0.5968 Acc: 0.9081 LR: 0.000421
Epoch [27/100] [100/228] Loss: 0.5753 Acc: 0.9163 LR: 0.000421
Epoch [27/100] [150/228] Loss: 0.5782 Acc: 0.9158 LR: 0.000421
Epoch [27/100] [200/228] Loss: 0.5832 Acc: 0.9170 LR: 0.000421
2026-06-18 16:41:40.532481: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:41:40.532581: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:41:44.849029: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:41:44.849126: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:41:49.146291: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:41:49.146389: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:41:53.460946: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:41:53.461071: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7877
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.7909 (174/220)
  类别 2 (中度裂缝): 0.7055 (206/292)
  类别 3 (重度裂缝): 0.7976 (134/168)
  类别 4 (严重裂缝): 0.6989 (65/93)

Epoch [27/100] 总结:
  Train Loss: 0.5819, Train Acc: 0.9168
  Val Loss: 0.8329, Val Acc: 0.7877
  LR: 0.000415

2026-06-18 16:42:00.068315: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:42:00.068414: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:42:04.477948: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:42:04.478056: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:42:08.883390: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:42:08.883503: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:42:13.046023: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:42:13.046121: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [28/100] [50/228] Loss: 0.5639 Acc: 0.9269 LR: 0.000415
Epoch [28/100] [100/228] Loss: 0.5626 Acc: 0.9247 LR: 0.000415
Epoch [28/100] [150/228] Loss: 0.5615 Acc: 0.9237 LR: 0.000415
Epoch [28/100] [200/228] Loss: 0.5663 Acc: 0.9200 LR: 0.000415
2026-06-18 16:42:29.620334: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:42:29.620443: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:42:33.602471: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:42:33.602587: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:42:37.562719: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:42:37.562822: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:42:41.532605: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:42:41.532708: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8228
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.9000 (198/220)
  类别 2 (中度裂缝): 0.7671 (224/292)
  类别 3 (重度裂缝): 0.7143 (120/168)
  类别 4 (严重裂缝): 0.7419 (69/93)

Epoch [28/100] 总结:
  Train Loss: 0.5692, Train Acc: 0.9180
  Val Loss: 0.8547, Val Acc: 0.8228
  LR: 0.000410

2026-06-18 16:42:47.543632: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:42:47.543731: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:42:51.581059: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:42:51.581167: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:42:55.590805: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:42:55.590899: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:42:59.594205: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:42:59.594305: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [29/100] [50/228] Loss: 0.5680 Acc: 0.9306 LR: 0.000410
Epoch [29/100] [100/228] Loss: 0.5588 Acc: 0.9284 LR: 0.000410
Epoch [29/100] [150/228] Loss: 0.5591 Acc: 0.9279 LR: 0.000410
Epoch [29/100] [200/228] Loss: 0.5651 Acc: 0.9237 LR: 0.000410
2026-06-18 16:43:15.772993: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:43:15.773101: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:43:19.699638: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:43:19.699735: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:43:23.625605: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:43:23.625707: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:43:27.529273: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:43:27.529379: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7834
  类别 0 (无裂缝): 0.9858 (139/141)
  类别 1 (轻度裂缝): 0.8773 (193/220)
  类别 2 (中度裂缝): 0.5925 (173/292)
  类别 3 (重度裂缝): 0.8095 (136/168)
  类别 4 (严重裂缝): 0.8065 (75/93)

Epoch [29/100] 总结:
  Train Loss: 0.5683, Train Acc: 0.9208
  Val Loss: 0.8863, Val Acc: 0.7834
  LR: 0.000403

2026-06-18 16:43:33.431017: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:43:33.431124: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:43:37.353751: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:43:37.353847: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:43:41.269286: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:43:41.269391: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:43:45.171120: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:43:45.171216: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [30/100] [50/228] Loss: 0.5355 Acc: 0.9406 LR: 0.000403
Epoch [30/100] [100/228] Loss: 0.5473 Acc: 0.9334 LR: 0.000403
Epoch [30/100] [150/228] Loss: 0.5484 Acc: 0.9325 LR: 0.000403
Epoch [30/100] [200/228] Loss: 0.5476 Acc: 0.9342 LR: 0.000403
2026-06-18 16:44:01.206384: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:44:01.206488: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:44:05.155350: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:44:05.155457: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:44:09.086962: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:44:09.087055: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:44:12.990818: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:44:12.990926: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7987
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.7591 (167/220)
  类别 2 (中度裂缝): 0.8082 (236/292)
  类别 3 (重度裂缝): 0.6786 (114/168)
  类别 4 (严重裂缝): 0.7742 (72/93)

Epoch [30/100] 总结:
  Train Loss: 0.5525, Train Acc: 0.9316
  Val Loss: 0.8592, Val Acc: 0.7987
  LR: 0.000397

2026-06-18 16:44:18.924201: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:44:18.924309: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:44:22.922815: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:44:22.922918: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:44:26.935496: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:44:26.935590: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:44:30.877616: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:44:30.877723: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [31/100] [50/228] Loss: 0.5378 Acc: 0.9406 LR: 0.000397
Epoch [31/100] [100/228] Loss: 0.5626 Acc: 0.9303 LR: 0.000397
Epoch [31/100] [150/228] Loss: 0.5605 Acc: 0.9292 LR: 0.000397
Epoch [31/100] [200/228] Loss: 0.5589 Acc: 0.9306 LR: 0.000397
2026-06-18 16:44:46.858113: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:44:46.858218: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:44:50.806419: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:44:50.806524: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:44:54.723851: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:44:54.723956: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:44:58.661229: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:44:58.661340: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8249
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8727 (192/220)
  类别 2 (中度裂缝): 0.8116 (237/292)
  类别 3 (重度裂缝): 0.6905 (116/168)
  类别 4 (严重裂缝): 0.7312 (68/93)

Epoch [31/100] 总结:
  Train Loss: 0.5602, Train Acc: 0.9291
  Val Loss: 0.8224, Val Acc: 0.8249
  LR: 0.000391

2026-06-18 16:45:04.529206: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:45:04.529304: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:45:08.459106: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:45:08.459200: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:45:12.424563: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:45:12.424671: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:45:16.340144: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:45:16.340252: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [32/100] [50/228] Loss: 0.5327 Acc: 0.9306 LR: 0.000391
Epoch [32/100] [100/228] Loss: 0.5385 Acc: 0.9341 LR: 0.000391
Epoch [32/100] [150/228] Loss: 0.5390 Acc: 0.9365 LR: 0.000391
Epoch [32/100] [200/228] Loss: 0.5383 Acc: 0.9361 LR: 0.000391
2026-06-18 16:45:32.209775: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:45:32.209869: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:45:36.168388: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:45:36.168500: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:45:40.096411: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:45:40.096516: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:45:44.024580: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:45:44.024699: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7757
  类别 0 (无裂缝): 0.9716 (137/141)
  类别 1 (轻度裂缝): 0.9182 (202/220)
  类别 2 (中度裂缝): 0.6096 (178/292)
  类别 3 (重度裂缝): 0.7798 (131/168)
  类别 4 (严重裂缝): 0.6559 (61/93)

Epoch [32/100] 总结:
  Train Loss: 0.5368, Train Acc: 0.9370
  Val Loss: 0.9194, Val Acc: 0.7757
  LR: 0.000384

2026-06-18 16:45:49.869643: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:45:49.869743: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:45:53.799287: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:45:53.799385: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:45:57.729894: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:45:57.730007: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:46:01.684373: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:46:01.684478: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [33/100] [50/228] Loss: 0.5176 Acc: 0.9456 LR: 0.000384
Epoch [33/100] [100/228] Loss: 0.5284 Acc: 0.9384 LR: 0.000384
Epoch [33/100] [150/228] Loss: 0.5341 Acc: 0.9375 LR: 0.000384
Epoch [33/100] [200/228] Loss: 0.5363 Acc: 0.9358 LR: 0.000384
2026-06-18 16:46:17.611317: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:46:17.611415: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:46:21.535427: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:46:21.535539: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:46:25.467104: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:46:25.467219: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:46:29.404211: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:46:29.404313: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8020
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8636 (190/220)
  类别 2 (中度裂缝): 0.7397 (216/292)
  类别 3 (重度裂缝): 0.7619 (128/168)
  类别 4 (严重裂缝): 0.6237 (58/93)

Epoch [33/100] 总结:
  Train Loss: 0.5400, Train Acc: 0.9341
  Val Loss: 0.8620, Val Acc: 0.8020
  LR: 0.000378

2026-06-18 16:46:35.348261: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:46:35.348358: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:46:39.293246: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:46:39.293340: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:46:43.301415: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:46:43.301525: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:46:47.320698: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:46:47.320806: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [34/100] [50/228] Loss: 0.5042 Acc: 0.9531 LR: 0.000378
Epoch [34/100] [100/228] Loss: 0.5190 Acc: 0.9466 LR: 0.000378
Epoch [34/100] [150/228] Loss: 0.5273 Acc: 0.9390 LR: 0.000378
Epoch [34/100] [200/228] Loss: 0.5233 Acc: 0.9419 LR: 0.000378
2026-06-18 16:47:05.710237: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:47:05.710333: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:47:10.063873: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:47:10.063981: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:47:14.409766: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:47:14.409864: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:47:18.847894: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:47:18.848001: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8162
  类别 0 (无裂缝): 0.9858 (139/141)
  类别 1 (轻度裂缝): 0.8773 (193/220)
  类别 2 (中度裂缝): 0.8014 (234/292)
  类别 3 (重度裂缝): 0.7262 (122/168)
  类别 4 (严重裂缝): 0.6237 (58/93)

Epoch [34/100] 总结:
  Train Loss: 0.5265, Train Acc: 0.9400
  Val Loss: 0.8767, Val Acc: 0.8162
  LR: 0.000371

2026-06-18 16:47:25.624201: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:47:25.624297: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:47:30.055373: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:47:30.055483: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:47:34.505686: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:47:34.505790: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:47:38.949163: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:47:38.949271: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [35/100] [50/228] Loss: 0.5362 Acc: 0.9375 LR: 0.000371
Epoch [35/100] [100/228] Loss: 0.5227 Acc: 0.9428 LR: 0.000371
Epoch [35/100] [150/228] Loss: 0.5258 Acc: 0.9427 LR: 0.000371
Epoch [35/100] [200/228] Loss: 0.5265 Acc: 0.9448 LR: 0.000371
2026-06-18 16:47:57.529425: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:47:57.529527: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:48:01.880514: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:48:01.880624: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:48:06.198179: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:48:06.198294: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:48:10.509665: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:48:10.509774: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7987
  类别 0 (无裂缝): 0.9858 (139/141)
  类别 1 (轻度裂缝): 0.9091 (200/220)
  类别 2 (中度裂缝): 0.6986 (204/292)
  类别 3 (重度裂缝): 0.7262 (122/168)
  类别 4 (严重裂缝): 0.6989 (65/93)

Epoch [35/100] 总结:
  Train Loss: 0.5259, Train Acc: 0.9456
  Val Loss: 0.8848, Val Acc: 0.7987
  LR: 0.000364

2026-06-18 16:48:17.149409: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:48:17.149519: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:48:21.467647: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:48:21.467755: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:48:25.718681: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:48:25.718788: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:48:30.025600: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:48:30.025727: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [36/100] [50/228] Loss: 0.5091 Acc: 0.9519 LR: 0.000364
Epoch [36/100] [100/228] Loss: 0.5092 Acc: 0.9475 LR: 0.000364
Epoch [36/100] [150/228] Loss: 0.5109 Acc: 0.9475 LR: 0.000364
Epoch [36/100] [200/228] Loss: 0.5148 Acc: 0.9450 LR: 0.000364
2026-06-18 16:48:48.055999: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:48:48.056110: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:48:52.301786: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:48:52.301891: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:48:56.505529: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:48:56.505625: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:49:00.739060: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:49:00.739170: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.7998
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.9227 (203/220)
  类别 2 (中度裂缝): 0.7021 (205/292)
  类别 3 (重度裂缝): 0.6964 (117/168)
  类别 4 (严重裂缝): 0.6989 (65/93)

Epoch [36/100] 总结:
  Train Loss: 0.5155, Train Acc: 0.9452
  Val Loss: 0.8794, Val Acc: 0.7998
  LR: 0.000357

2026-06-18 16:49:07.203344: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:49:07.203443: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:49:11.412580: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:49:11.412703: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:49:15.633772: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:49:15.633868: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:49:19.861185: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:49:19.861285: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [37/100] [50/228] Loss: 0.5076 Acc: 0.9563 LR: 0.000357
Epoch [37/100] [100/228] Loss: 0.5031 Acc: 0.9591 LR: 0.000357
Epoch [37/100] [150/228] Loss: 0.5068 Acc: 0.9546 LR: 0.000357
Epoch [37/100] [200/228] Loss: 0.5065 Acc: 0.9547 LR: 0.000357
2026-06-18 16:49:37.838239: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:49:37.838342: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:49:42.059668: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:49:42.059777: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:49:46.272070: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:49:46.272181: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:49:50.640446: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:49:50.640556: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8162
  类别 0 (无裂缝): 0.9929 (140/141)
  类别 1 (轻度裂缝): 0.8955 (197/220)
  类别 2 (中度裂缝): 0.7432 (217/292)
  类别 3 (重度裂缝): 0.7381 (124/168)
  类别 4 (严重裂缝): 0.7312 (68/93)

Epoch [37/100] 总结:
  Train Loss: 0.5078, Train Acc: 0.9534
  Val Loss: 0.8469, Val Acc: 0.8162
  LR: 0.000350

2026-06-18 16:49:57.065059: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:49:57.065164: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:50:01.249958: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:50:01.250059: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:50:05.448427: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:50:05.448549: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:50:09.651586: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:50:09.651682: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Epoch [38/100] [50/228] Loss: 0.5110 Acc: 0.9544 LR: 0.000350
Epoch [38/100] [100/228] Loss: 0.5146 Acc: 0.9516 LR: 0.000350
Epoch [38/100] [150/228] Loss: 0.5142 Acc: 0.9510 LR: 0.000350
Epoch [38/100] [200/228] Loss: 0.5125 Acc: 0.9523 LR: 0.000350
2026-06-18 16:50:27.673699: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:50:27.673806: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:50:31.899152: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:50:31.899263: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:50:36.111869: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:50:36.111972: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:50:40.373702: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:50:40.373824: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

VAL 结果:
总体准确率: 0.8228
  类别 0 (无裂缝): 1.0000 (141/141)
  类别 1 (轻度裂缝): 0.8500 (187/220)
  类别 2 (中度裂缝): 0.7705 (225/292)
  类别 3 (重度裂缝): 0.7798 (131/168)
  类别 4 (严重裂缝): 0.7312 (68/93)

Epoch [38/100] 总结:
  Train Loss: 0.5135, Train Acc: 0.9515
  Val Loss: 0.8275, Val Acc: 0.8228
  LR: 0.000342


早停触发！连续 20 个 epoch 无提升

============================================================
训练完成！
总耗时: 30.81 分钟
最佳验证准确率: 0.8337 (Epoch 18)
============================================================

在测试集上评估...
2026-06-18 16:50:46.788180: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:50:46.788281: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:50:50.973642: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:50:50.973743: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:50:55.173880: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:50:55.173979: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2026-06-18 16:50:59.390988: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
2026-06-18 16:50:59.391093: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.

TEST 结果:
总体准确率: 0.8348
  类别 0 (无裂缝): 1.0000 (142/142)
  类别 1 (轻度裂缝): 0.8054 (178/221)
  类别 2 (中度裂缝): 0.7986 (234/293)
  类别 3 (重度裂缝): 0.8047 (136/169)
  类别 4 (严重裂缝): 0.8211 (78/95)

测试集准确率: 0.8348

进程已结束，退出代码为 0
