import argparse
import os.path as osp
import sys
sys.path.insert(0, '.')

import torch
import onnxsim
import onnx
from lib.models import model_factory
from configs import set_cfg_from_file

torch.set_grad_enabled(False)

parse = argparse.ArgumentParser()
parse.add_argument('--config', dest='config', type=str,
        default='configs/bisenetv2.py',)
parse.add_argument('--weight-path', dest='weight_pth', type=str,
        default='D:\BiSeNet-master\BiSeNet-master\weights\model_final.pth')
parse.add_argument('--outpath', dest='out_pth', type=str,
        default='bisenetv2_crack.onnx')
parse.add_argument('--aux-mode', dest='aux_mode', type=str,
        default='pred')
args = parse.parse_args()

cfg = set_cfg_from_file(args.config)
if cfg.use_sync_bn: cfg.use_sync_bn = False

# 加载模型
net = model_factory[cfg.model_type](cfg.n_cats, aux_mode=args.aux_mode)
net.load_state_dict(torch.load(args.weight_pth, map_location='cpu',
                               weights_only=True), strict=False)
net.eval()

# 固定batch=1，删除动态shape代码
h, w = cfg.cropsize
dummy_input = torch.randn(1, 3, h, w)
input_names = ['input_image']
output_names = ['preds']

# 导出ONNX，opset改为17，关闭动态
torch.onnx.export(
    net,
    dummy_input,
    args.out_pth,
    input_names=input_names,
    output_names=output_names,
    do_constant_folding=True,
    verbose=False,
    opset_version=17,  # RKNN2.3.2稳定版本
    external_data=False
)
print(f"原始ONNX导出完成：{args.out_pth}")

# 新增：onnxsim简化模型（关键，减少量化噪点）
model_onnx = onnx.load(args.out_pth)
model_simplified, check_success = onnxsim.simplify(model_onnx)
assert check_success, "ONNX模型简化失败，存在不兼容算子"

# 覆盖保存简化后的onnx（给RKNN转换专用）
onnx.save(model_simplified, args.out_pth)
print(f"✅ 简化完成，最终RKNN可用模型：{args.out_pth}")