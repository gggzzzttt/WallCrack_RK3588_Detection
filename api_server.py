#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
裂缝分割+分类推理服务
基于FastAPI实现的RESTful API接口

功能：
1. 接收上传的图片
2. 进行裂缝分割和分类
3. 返回结果图片路径
4. 支持批量处理
5. 模型权重只加载一次（启动时）

使用方法:
    uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload

接口文档:
    http://localhost:8000/docs  (Swagger UI)
    http://localhost:8000/redoc (ReDoc)
"""

import os
import sys
import uuid
import shutil
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

import torch
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 确保项目根目录在sys.path中
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

# 导入推理模块
from inference_crack import CrackInferencePipeline


# ============ 配置 ============
class Config:
    """全局配置"""
    # 模型配置
    SEG_CONFIG = 'configs/bisenetv2_crack.py'
    SEG_WEIGHT = 'res_3/crack_bisenetv2/model_best.pth'
    CLS_WEIGHT = 'crack_classifier/res/crack_classifier/mobilenetv3_small/model_best.pth'

    # 设备
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    # 文件存储目录
    UPLOAD_DIR = PROJECT_ROOT / 'uploads'           # 上传文件临时存储
    RESULT_DIR = PROJECT_ROOT / 'api_results'       # API推理结果存储
    TEMP_DIR = PROJECT_ROOT / 'temp'                # 临时文件目录

    # 允许的图片格式
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}

    # 最大文件大小（10MB）
    MAX_FILE_SIZE = 10 * 1024 * 1024


config = Config()

# 创建必要的目录
for dir_path in [config.UPLOAD_DIR, config.RESULT_DIR, config.TEMP_DIR]:
    dir_path.mkdir(exist_ok=True)


# ============ 全局变量（模型实例）============
pipeline: Optional[CrackInferencePipeline] = None


def get_pipeline() -> CrackInferencePipeline:
    """
    获取或初始化推理管道（单例模式）

    Returns:
        CrackInferencePipeline: 推理管道实例
    """
    global pipeline
    if pipeline is None:
        print("\n" + "=" * 60)
        print("首次加载模型...")
        print("=" * 60)

        pipeline = CrackInferencePipeline(
            seg_config=config.SEG_CONFIG,
            seg_weight=config.SEG_WEIGHT,
            cls_weight=config.CLS_WEIGHT,
            device=config.DEVICE
        )

        print("✓ 模型加载完成！")
        print("=" * 60 + "\n")

    return pipeline


# ============ Lifespan 事件处理器（替代已弃用的 @app.on_event）============
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global pipeline

    # 启动时：加载模型
    try:
        print("\n" + "=" * 60)
        print("正在启动裂缝检测服务...")
        print("=" * 60)

        # 预加载模型
        get_pipeline()

        print(f"\n✓ 服务启动成功!")
        print(f"  设备: {config.DEVICE}")
        print(f"  上传目录: {config.UPLOAD_DIR}")
        print(f"  结果目录: {config.RESULT_DIR}")
        print(f"  接口文档: http://localhost:8000/docs")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n✗ 服务启动失败: {e}")
        raise e

    yield  # 应用运行中...

    # 关闭时：清理资源（如果需要）
    print("\n正在关闭服务...")
    # 这里可以添加清理代码，比如释放GPU内存等
    print("✓ 服务已关闭")


# ============ FastAPI应用 ============
app = FastAPI(
    title="裂缝分割+分类推理服务",
    description="""
    基于BiSeNetV2和MobileNetV3的裂缝检测与分类API服务

    ## 功能特点
    - **裂缝分割**：使用BiSeNetV2进行精确的裂缝区域分割
    - **裂缝分类**：使用MobileNetV3将裂缝分为5个等级（无/轻度/中度/重度/严重）
    - **可视化输出**：生成包含原图、掩码、叠加结果的对比图
    - **中文支持**：支持中文标签显示

    ## 分类等级说明
    - **Level 0 (无裂缝)**：绿色标注
    - **Level 1 (轻度裂缝)**：青色标注
    - **Level 2 (中度裂缝)**：橙色标注
    - **Level 3 (重度裂缝)**：红色标注
    - **Level 4 (严重裂缝)**：深红色标注
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan  # 使用新的 lifespan 事件处理器
)

# CORS中间件（允许跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ 辅助函数 ============
def validate_image_file(filename: str) -> bool:
    """
    验证文件扩展名是否为允许的图片格式

    Args:
        filename: 文件名

    Returns:
        bool: 是否为有效图片格式
    """
    return Path(filename).suffix.lower() in config.ALLOWED_EXTENSIONS


async def save_upload_file(upload_file: UploadFile) -> Path:
    """
    保存上传的文件到临时目录

    Args:
        upload_file: 上传的文件对象

    Returns:
        Path: 保存后的文件路径
    """
    # 生成唯一文件名
    file_ext = Path(upload_file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = config.TEMP_DIR / unique_filename

    # 保存文件
    with open(file_path, "wb") as buffer:
        content = await upload_file.read()
        if len(content) > config.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"文件大小超过限制 ({config.MAX_FILE_SIZE / 1024 / 1024}MB)")
        buffer.write(content)

    return file_path


def cleanup_temp_files(file_paths: List[Path]):
    """
    清理临时文件

    Args:
        file_paths: 要删除的文件路径列表
    """
    for path in file_paths:
        try:
            if path.exists():
                path.unlink()
        except Exception as e:
            print(f"警告: 无法删除临时文件 {path}: {e}")


# ============ 数据模型 ============
class InferenceResponse(BaseModel):
    """推理响应数据模型"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class BatchInferenceResponse(BaseModel):
    """批量推理响应数据模型"""
    success: bool
    message: str
    total: int = 0
    success_count: int = 0
    failed_count: int = 0
    results: List[Dict[str, Any]] = []


class HealthCheck(BaseModel):
    """健康检查响应"""
    status: str
    device: str
    model_loaded: bool
    timestamp: str


# ============ API接口 ============

@app.get("/", tags=["根路径"])
async def root():
    """根路径 - 返回服务信息"""
    return {
        "service": "裂缝分割+分类推理服务",
        "version": "1.0.0",
        "description": "基于BiSeNetV2和MobileNetV3的裂缝检测与分类API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthCheck, tags=["系统"])
async def health_check():
    """
    健康检查接口

    检查服务状态、设备信息、模型是否已加载等
    """
    return HealthCheck(
        status="healthy" if pipeline else "initializing",
        device=config.DEVICE,
        model_loaded=pipeline is not None,
        timestamp=datetime.now().isoformat()
    )


@app.post("/infer", response_model=InferenceResponse, tags=["推理"])
async def infer_single_image(
    file: UploadFile = File(..., description="待识别的裂缝图片")
):
    """
    单张图片推理接口

    上传一张裂缝图片，返回分割和分类结果

    - **输入**: 图片文件 (png/jpg/jpeg/bmp/tiff, 最大10MB)
    - **输出**: 分割掩码路径、结果图片路径、分类信息、JSON详细结果

    ## 示例请求

    ```python
    import requests

    url = "http://localhost:8000/infer"
    files = {"file": open("crack_image.png", "rb")}
    response = requests.post(url, files=files)
    result = response.json()
    ```
    """
    temp_files = []

    try:
        # 1. 验证文件
        if not file.filename:
            raise HTTPException(status_code=400, detail="未提供文件名")

        if not validate_image_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式。支持的格式: {config.ALLOWED_EXTENSIONS}"
            )

        # 2. 保存上传的文件
        file_path = await save_upload_file(file)
        temp_files.append(file_path)

        print(f"\n[API] 收到图片: {file.filename} ({file_path.name})")

        # 3. 执行推理
        inference_pipeline = get_pipeline()
        result = inference_pipeline.inference(str(file_path), str(config.RESULT_DIR))

        # 4. 构建响应
        response_data = {
            "original_filename": file.filename,
            "image_size": result["image_size"],
            "segmentation": {
                "mask_path": result["segmentation"]["mask_path"],
                "crack_pixels": result["segmentation"]["crack_pixels"],
                "total_pixels": result["segmentation"]["total_pixels"],
                "crack_ratio": f"{result['segmentation']['crack_ratio']:.4f}"
            },
            "classification": {
                "class_id": result["classification"]["class_id"],
                "class_name": result["classification"]["class_name"],
                "confidence": f"{result['classification']['confidence']:.4f}"
            },
            "output_files": {
                "result_image": result["result_image"],      # 可视化结果图
                "mask_image": result["segmentation"]["mask_path"],  # 分割掩码
                "json_result": result.get("json_result", "")  # JSON详细结果
            }
        }

        print(f"[API] 推理完成: {result['classification']['class_name']} "
              f"(置信度: {result['classification']['confidence']:.2%})")

        return InferenceResponse(
            success=True,
            message="推理成功",
            data=response_data
        )

    except HTTPException as he:
        raise he

    except Exception as e:
        error_msg = f"推理失败: {str(e)}"
        print(f"[API] 错误: {error_msg}")
        return InferenceResponse(
            success=False,
            message=error_msg
        )

    finally:
        # 清理临时文件
        cleanup_temp_files(temp_files)


@app.post("/infer/batch", response_model=BatchInferenceResponse, tags=["推理"])
async def infer_batch_images(
    files: List[UploadFile] = File(..., description="多张待识别的裂缝图片"),
):
    """
    批量图片推理接口

    同时上传多张裂缝图片，批量返回所有结果

    - **输入**: 多张图片文件 (最多20张)
    - **输出**: 所有图片的推理结果列表

    ## 示例请求

    ```python
    import requests

    url = "http://localhost:8000/infer/batch"
    files = [
        ("files", open("image1.png", "rb")),
        ("files", open("image2.png", "rb")),
        ("files", open("image3.png", "rb")),
    ]
    response = requests.post(url, files=files)
    results = response.json()
    ```
    """
    if len(files) > 20:
        raise HTTPException(status_code=400, detail="单次最多处理20张图片")

    if len(files) == 0:
        raise HTTPException(status_code=400, detail="请至少上传1张图片")

    temp_files = []
    results = []
    success_count = 0
    failed_count = 0

    try:
        # 预加载模型（如果还没加载）
        inference_pipeline = get_pipeline()

        print(f"\n[API] 收到批量推理请求: {len(files)} 张图片")

        for i, file in enumerate(files, 1):
            single_result = {
                "index": i,
                "filename": file.filename or f"unknown_{i}",
                "success": False,
                "error": None,
                "data": None
            }

            try:
                # 验证文件
                if not file.filename or not validate_image_file(file.filename):
                    single_result["error"] = f"不支持的文件格式: {file.filename}"
                    failed_count += 1
                    results.append(single_result)
                    continue

                # 保存文件
                file_path = await save_upload_file(file)
                temp_files.append(file_path)

                print(f"[API] 处理 [{i}/{len(files)}]: {file.filename}")

                # 执行推理
                result = inference_pipeline.inference(str(file_path), str(config.RESULT_DIR))

                # 构建单个结果
                single_result.update({
                    "success": True,
                    "data": {
                        "original_filename": file.filename,
                        "classification": {
                            "class_id": result["classification"]["class_id"],
                            "class_name": result["classification"]["class_name"],
                            "confidence": f"{result['classification']['confidence']:.4f}"
                        },
                        "segmentation": {
                            "crack_ratio": f"{result['segmentation']['crack_ratio']:.4f}"
                        },
                        "output_files": {
                            "result_image": result["result_image"],
                            "mask_image": result["segmentation"]["mask_path"]
                        }
                    }
                })

                success_count += 1

            except Exception as e:
                single_result["error"] = str(e)
                failed_count += 1
                print(f"[API] 错误 [{i}]: {e}")

            results.append(single_result)

        # 统计各分类数量
        class_stats = {}
        for r in results:
            if r["success"] and r["data"]:
                class_name = r["data"]["classification"]["class_name"]
                class_stats[class_name] = class_stats.get(class_name, 0) + 1

        print(f"[API] 批量推理完成: 成功 {success_count}, 失败 {failed_count}")

        return BatchInferenceResponse(
            success=True,
            message=f"批量推理完成: 成功 {success_count}, 失败 {failed_count}",
            total=len(files),
            success_count=success_count,
            failed_count=failed_count,
            results=results
        )

    except Exception as e:
        error_msg = f"批量推理失败: {str(e)}"
        print(f"[API] 错误: {error_msg}")
        return BatchInferenceResponse(
            success=False,
            message=error_msg,
            total=len(files),
            success_count=success_count,
            failed_count=len(files),
            results=results
        )

    finally:
        # 清理临时文件
        cleanup_temp_files(temp_files)


@app.get("/results/{filename}", tags=["文件"])
async def get_result_file(filename: str):
    """
    获取结果文件接口

    通过文件名获取生成的结果图片或JSON文件

    - **参数**: filename - 文件名（如: xxx_result_20260619_120000.jpg）
    - **返回**: 文件内容
    """
    # 安全性检查：防止路径遍历攻击
    safe_filename = os.path.basename(filename)
    file_path = config.RESULT_DIR / safe_filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"文件不存在: {safe_filename}")

    # 根据文件类型返回不同的Content-Type
    from fastapi.responses import FileResponse

    content_type = "application/octet-stream"
    if safe_filename.endswith(('.png', '.jpg', '.jpeg')):
        content_type = "image/*"
    elif safe_filename.endswith('.json'):
        content_type = "application/json"

    return FileResponse(
        path=str(file_path),
        media_type=content_type,
        filename=safe_filename
    )


@app.get("/list-results", tags=["文件"])
async def list_results(
    limit: int = Query(default=20, ge=1, le=100, description="返回结果数量限制"),
    offset: int = Query(default=0, ge=0, description="偏移量")
):
    """
    列出最近的结果文件

    返回最近生成的推理结果文件列表
    """
    if not config.RESULT_DIR.exists():
        return {"total": 0, "results": []}

    # 获取所有结果文件
    all_files = sorted(
        config.RESULT_DIR.glob("*.*"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    # 分页
    paginated_files = all_files[offset:offset+limit]

    results = []
    for file_path in paginated_files:
        stat = file_path.stat()
        results.append({
            "filename": file_path.name,
            "size": stat.st_size,
            "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "url": f"/results/{file_path.name}"
        })

    return {
        "total": len(all_files),
        "limit": limit,
        "offset": offset,
        "results": results
    }


if __name__ == '__main__':
    import uvicorn

    print("\n" + "=" * 80)
    print("裂缝分割+分类推理服务")
    print("=" * 80)
    print("\n启动方式:")
    print("  方式1: python api_server.py")
    print("  方式2: uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload")
    print("\n接口文档:")
    print("  Swagger UI: http://localhost:8000/docs")
    print("  ReDoc:      http://localhost:8000/redoc")
    print("=" * 80 + "\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
        # 注意：reload=True 只能通过命令行使用，不能在代码中直接设置
        # 如需热重载功能，请使用命令行启动：
        # uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
    )
