import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

import cv2
import numpy as np
import gc
from rknnlite.api import RKNNLite as RKNN

# ==================== 配置 ====================
SEG_RKNN = "bisenetv2_crack.rknn"
CLS_RKNN = "mobilenetv3_crack_cls.rknn"
CAM_ID = "/dev/video21"

SEG_INPUT_SIZE = (512, 512)
CLS_INPUT_SIZE = (224, 224)
SEG_MEAN = np.array([0.3257, 0.3690, 0.3223], dtype=np.float32)
SEG_STD  = np.array([0.2112, 0.2148, 0.2115], dtype=np.float32)
SEG_THRESH = 0.5

CLS_MEAN = np.array([0.485, 0.456, 0.406, 0.0], dtype=np.float32)
CLS_STD  = np.array([0.229, 0.224, 0.225, 1.0])

level_name = [
    "No Crack",
    "Very Slight Crack",
    "Slight Crack",
    "Moderate Crack",
    "Severe Crack"
]
# ==============================================

def letterbox_pad(img, target_w, target_h):
    h, w = img.shape[:2]
    scale = min(target_w / w, target_h / h)
    nw = int(w * scale)
    nh = int(h * scale)
    img_resize = cv2.resize(img, (nw, nh))
    pad_left = (target_w - nw) // 2
    pad_right = target_w - nw - pad_left
    pad_top = (target_h - nh) // 2
    pad_bottom = target_h - nh - pad_top
    img_pad = cv2.copyMakeBorder(img_resize, pad_top, pad_bottom, pad_left, pad_right,
                                  cv2.BORDER_CONSTANT, value=[114, 114, 114])
    return img_pad, pad_left, pad_top, pad_right, pad_bottom, scale

def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum()

def run_seg(orig_img, seg_rknn):
    h_o, w_o = orig_img.shape[:2]
    img_pad, pad_l, pad_t, pad_r, pad_b, s = letterbox_pad(orig_img, SEG_INPUT_SIZE[0], SEG_INPUT_SIZE[1])
    c_pad = img_pad.shape[2]
    if c_pad == 4:
        img_pad = img_pad[..., :3]
    img_rgb = cv2.cvtColor(img_pad, cv2.COLOR_BGR2RGB)
    img_rgb = img_rgb.astype(np.float32) / 255.0
    img_rgb = (img_rgb - SEG_MEAN) / SEG_STD
    input_seg = np.expand_dims(img_rgb, axis=0).astype(np.float32)

    seg_out = seg_rknn.inference(inputs=[input_seg])[0]
    _, c, H, W = seg_out.shape
    bg_logit = seg_out[0,0,:,:]
    crack_logit = seg_out[0,1,:,:]
    stack_logits = np.stack([bg_logit, crack_logit], axis=-1)
    exp_logits = np.exp(stack_logits - np.max(stack_logits, axis=-1, keepdims=True))
    prob = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)
    crack_prob = prob[:, :, 1]

    mask = np.zeros((H, W), dtype=np.uint8)
    mask[crack_prob > SEG_THRESH] = 255

    h_mask, w_mask = mask.shape
    x1 = pad_l
    x2 = w_mask - pad_r
    y1 = pad_t
    y2 = h_mask - pad_b
    
    mask_crop = mask[y1:y2, x1:x2]
    mask_origin = cv2.resize(mask_crop, (w_o, h_o), interpolation=cv2.INTER_NEAREST)

    del seg_out, crack_prob, bg_logit, crack_logit, stack_logits, exp_logits, prob
    gc.collect()
    return mask, mask_origin

def run_cls(mask, cls_rknn):
    mask_res = cv2.resize(mask, CLS_INPUT_SIZE)
    four_ch = np.stack([mask_res, mask_res, mask_res, mask_res], axis=-1)
    four_ch = four_ch.astype(np.float32) / 255.0
    four_ch = (four_ch - CLS_MEAN) / CLS_STD
    input_cls = np.expand_dims(four_ch.transpose(2,0,1), axis=0).astype(np.float32)

    cls_out = cls_rknn.inference(inputs=[input_cls])[0][0]
    prob_all = softmax(cls_out)
    pred_level = int(np.argmax(prob_all))
    conf = prob_all[pred_level] * 100
    if 0 <= pred_level < len(level_name):
        cls_text = level_name[pred_level]
    else:
        cls_text = "Unknown Crack Level"
    gc.collect()
    return cls_text, conf, pred_level

def draw_result(orig_img, mask_origin, cls_text, conf, pred_level):
    img1 = orig_img.copy()
    img2 = cv2.cvtColor(mask_origin, cv2.COLOR_GRAY2BGR)
    img3 = orig_img.copy()
    idx = mask_origin > 0
    img3[idx, 2] = np.clip(img3[idx, 2] + 100, 0, 255)

    target_h = max(img1.shape[0], img2.shape[0], img3.shape[0])
    def align_h(img):
        scale = target_h / img.shape[0]
        w = int(img.shape[1] * scale)
        return cv2.resize(img, (w, target_h))
    img1 = align_h(img1)
    img2 = align_h(img2)
    img3 = align_h(img3)
    combine = np.hstack([img1, img2, img3])

    # 稍微缩短整体图片长度，约为原来的 75%
    new_w = int(combine.shape[1] * 0.75)
    new_h = int(combine.shape[0] * 0.75)
    combine = cv2.resize(combine, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # 顶部显示栏加高，放大字号
    text = f"Class: {cls_text} (Level {pred_level}) - Confidence: {conf:.2f}%"
    top_h = 80
    top_bar = np.ones((top_h, combine.shape[1], 3), dtype=np.uint8) * 255

    # 顶部大字号
    cv2.putText(top_bar, text, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 0), 4)

    # 叠加图文字也放大
    cv2.putText(combine, f"Level {pred_level}: {cls_text} | Conf:{conf:.1f}%",
                (10, combine.shape[0] - 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 200), 3)

    final_img = np.vstack([top_bar, combine])

    return final_img

if __name__ == "__main__":
    print("===== 初始化双模型 =====")
    # 1.加载分割模型
    seg_rknn = RKNN()
    ret = seg_rknn.load_rknn(SEG_RKNN)
    if ret != 0:
        print("分割模型bisenetv2_crack.rknn加载失败！")
        exit()
    seg_rknn.init_runtime(core_mask=0)
    print("分割模型就绪")

    # 2.加载分类模型
    cls_rknn = RKNN()
    ret = cls_rknn.load_rknn(CLS_RKNN)
    if ret != 0:
        print("分类模型mobilenetv3_crack_cls.rknn加载失败！")
        seg_rknn.release()
        exit()
    cls_rknn.init_runtime(core_mask=0)
    print("分类模型就绪")

    # 打开USB摄像头
    cap = cv2.VideoCapture(CAM_ID, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not cap.isOpened():
        print(f"USB摄像头 {CAM_ID} 打开失败！")
        seg_rknn.release()
        cls_rknn.release()
        exit()

    print("冲刷摄像头初始黑帧，请等待2秒...")
    for _ in range(40):
        cap.read()

    print("====================操作说明====================")
    print("1. 实时视频每帧同步运行【分割+分类双模型】")
    print("2. 窗口三栏画面：原图 | 裂缝掩码 | 高亮叠加图，顶部显示裂缝等级")
    print("3. 画面保持原始比例，无强制压缩拉伸")
    print("4. 在视频窗口按下【回车键】直接关闭程序，释放两个模型")
    print("=================================================")

    # 可缩放窗口，不强制固定尺寸
    cv2.namedWindow("Crack Real-Time Detect", cv2.WINDOW_NORMAL)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 每帧实时推理
        mask, mask_origin = run_seg(frame, seg_rknn)
        cls_text, conf, pred_level = run_cls(mask, cls_rknn)
        show_img = draw_result(frame, mask_origin, cls_text, conf, pred_level)
        cv2.imshow("Crack Real-Time Detect", show_img)
        
        # 仅识别回车退出，无其他按键
        key = cv2.waitKey(1) & 0xFF
        if key == ord('\r'):
            print("收到回车退出指令，准备释放资源...")
            break

    # 释放全部资源
    cap.release()
    cv2.destroyAllWindows()
    seg_rknn.release()
    cls_rknn.release()
    print("程序正常退出，分割、分类双模型已释放")