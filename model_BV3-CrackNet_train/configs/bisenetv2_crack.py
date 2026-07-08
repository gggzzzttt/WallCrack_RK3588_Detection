# 裂缝分割配置文件
# BiSeNetV2 用于 CrackSeg9k 数据集

cfg = dict(
    # 模型配置
    model_type='bisenetv2',
    n_cats=2,  # 背景 + 裂缝
    num_aux_heads=4,  # BiSeNetV2 有 4 个辅助头

    # 训练配置
    lr_start=5e-3,
    weight_decay=5e-4,
    warmup_iters=1000,
    max_iter=40000,  # 训练迭代次数

    # 数据集配置
    dataset='CustomerDataset',
    im_root='./date',
    train_im_anns='./date/Final_Masks/train.txt',
    val_im_anns='./date/Final_Masks/test.txt',

    # 数据增强
    scales=[0.5, 2.0],  # 随机缩放范围
    cropsize=[512, 512],  # 训练裁剪尺寸

    # 评估配置
    eval_crop=[512, 512],
    eval_scales=[1.0],  # 单尺度评估

    # 批处理配置
    ims_per_gpu=16,  # 每个 GPU 的 batch size
    eval_ims_per_gpu=16,  # 评估 batch size（增大可加速评估）

    # 混合精度训练
    use_fp16=True,
    use_sync_bn=False,

    # 损失函数配置（Focal Loss + Dice Loss）
    use_focal_dice=True,  # 启用 Focal + Dice Loss
    focal_gamma=2.0,      # Focal Loss 聚焦参数
    focal_weight=1.0,     # Focal Loss 权重
    dice_weight=1.0,      # Dice Loss 权重

    # 保存路径
    respth='./res/crack_bisenetv2',

    # 检查点保存间隔
    save_interval=2000,  # 每 2000 次迭代保存一次
    eval_interval=1000,  # 每 1000 次迭代评估一次
)
