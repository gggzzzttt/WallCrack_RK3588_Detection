#!/bin/bash
# 裂缝分割训练启动脚本

# 单 GPU 训练
# python tools/train_crack.py --config configs/bisenetv2_crack.py

# 多 GPU 训练 (2 卡)
# torchrun --nproc_per_node=2 tools/train_crack.py --config configs/bisenetv2_crack.py

# 从检查点恢复训练
# python tools/train_crack.py --config configs/bisenetv2_crack.py --resume res/crack_bisenetv2/checkpoints/checkpoint_2000.pth

# 从预训练权重微调
# python tools/train_crack.py --config configs/bisenetv2_crack.py --finetune-from res/model_final.pth

echo "请使用以下命令之一启动训练:"
echo ""
echo "单 GPU 训练:"
echo "  python tools/train_crack.py --config configs/bisenetv2_crack.py"
echo ""
echo "多 GPU 训练 (2 卡):"
echo "  torchrun --nproc_per_node=2 tools/train_crack.py --config configs/bisenetv2_crack.py"
echo ""
echo "从检查点恢复:"
echo "  python tools/train_crack.py --config configs/bisenetv2_crack.py --resume res/crack_bisenetv2/checkpoints/checkpoint_2000.pth"
