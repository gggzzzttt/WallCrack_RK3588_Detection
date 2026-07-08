"""
裂缝分类训练配置
"""

import os

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    # 数据路径（使用相对路径）
    data_root = os.path.join(PROJECT_ROOT, "mobile_date")
    image_dir = os.path.join(PROJECT_ROOT, "date", "Images")  # 原图目录
    mask_dir = os.path.join(PROJECT_ROOT, "mobile_date")   # 掩码目录
    split_dir = os.path.join(PROJECT_ROOT, "crack_classifier", "data_splits")

    # 保存路径
    save_root = "./res/crack_classifier"
    model_name = "mobilenetv3_small"

    # 模型参数
    num_classes = 5  # 0-4级裂缝
    input_size = (224, 224)
    use_mask = True  # 是否使用掩码作为额外输入通道

    # 训练参数
    epochs = 100
    batch_size = 32
    num_workers = 4

    # 优化器
    optimizer = "adam"
    lr = 5e-4  # 降低学习率
    weight_decay = 5e-4  # 增加权重衰减

    # 类别加权损失（重点提升类别3）
    class_weights = [0.7, 0.9, 1.0, 1.8, 1.4]  # 类别3权重最高

    # 标签平滑
    label_smoothing = 0.1

    # 早停
    early_stopping_patience = 20  # 增加patience

    # 学习率调度
    scheduler = "cosine"  # cosine / step / plateau
    warmup_epochs = 5
    min_lr = 1e-6

    # 数据增强
    train_augmentation = True
    val_augmentation = False

    # 其他
    use_fp16 = False  # 分类任务通常不需要混合精度
    seed = 42
    print_freq = 50  # 每 N 个 batch 打印一次

    @classmethod
    def get_class_names(cls):
        return ["无裂缝", "轻度裂缝", "中度裂缝", "重度裂缝", "严重裂缝"]

    @classmethod
    def get_save_path(cls):
        save_dir = os.path.join(cls.save_root, cls.model_name)
        os.makedirs(save_dir, exist_ok=True)
        return save_dir
