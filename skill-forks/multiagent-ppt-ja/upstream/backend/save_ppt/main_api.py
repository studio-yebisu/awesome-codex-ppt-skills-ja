#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/7/17 15:07
# @File  : main_api.py.py
# @Author: johnson
# @Contact : github: johnson7788
# @Desc  :

# main.py
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
import logging

# 从 ppt_generator 模块导入生成器函数
from ppt_generator import start_generate_presentation

# 配置日志（确保FastAPI也能使用日志）
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PPT Generation API",
    description="API for generating PowerPoint presentations from structured JSON data.",
    version="1.0.0",
)
app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


# --- 定义 Pydantic 模型以验证传入的 JSON 数据 ---

class RootImage(BaseModel):
    url: str
    query: Optional[str] = None  # 用于DIO或其他查询信息
    background: bool = False  # 是否是背景图，如果为True则不单独创建图片幻灯片
    alt: Optional[str] = None  # 作为图片描述


class ContentChild(BaseModel):
    text: str


class ContentBlock(BaseModel):
    type: str  # e.g., "h1", "p", "bullets", "bullet", "h3"
    children: List[Dict[str, Any]]  # 使用 Dict[str, Any] 处理嵌套的复杂结构，因为内部结构多变


class SectionData(BaseModel):
    id: str
    content: List[ContentBlock]
    rootImage: Optional[RootImage] = None
    layoutType: Optional[str] = None
    alignment: Optional[str] = None


class PPTInput(BaseModel):
    sections: List[SectionData]
    references: Optional[List[str]] = None  # 参考文献列表


# --- 配置静态文件服务 ---
# 生成的PPT文件将保存在此目录，并由FastAPI提供静态访问
OUTPUT_PPT_DIR = "output_ppts"
if not os.path.exists(OUTPUT_PPT_DIR):
    os.makedirs(OUTPUT_PPT_DIR)
    logger.info(f"Created output directory: {OUTPUT_PPT_DIR}")

# 挂载静态文件目录
app.mount("/static_ppts", StaticFiles(directory=OUTPUT_PPT_DIR), name="static_ppts")

# --- 定义API端点 ---

@app.post("/generate-ppt", summary="Generate a PowerPoint presentation from JSON data")
async def generate_ppt(ppt_data: PPTInput):
    """
    根据前端提供的 JSON 数据生成 PowerPoint 演示文稿，并返回可访问的链接。

    **请求体示例:**
    ```json
    {
        "sections": [
            {
                "id": "...",
                "content": [...],
                "rootImage": {...}
            },
            ...
        ],
        "references": [...]
    }
    ```

    **响应体示例:**
    ```json
    {
        "message": "PPT generated successfully",
        "ppt_url": "http://localhost:8000/static_ppts/Your_Presentation_Title.pptx"
    }
    ```
    """
    logger.info("Received request to generate PPT.")

    # Pydantic模型会自动验证数据。将Pydantic对象转换为Python字典
    # model_dump() 是 Pydantic v2+ 的方法，旧版本使用 .dict()
    data_for_generator = ppt_data.model_dump(by_alias=True)  # by_alias=True 如果你的字段有别名

    try:
        # 调用核心的PPT生成逻辑
        output_filepath = start_generate_presentation(data_for_generator)
        output_filepath_name = os.path.basename(output_filepath)
        output_filepath_url = os.path.join(OUTER_IP, "static_ppts", output_filepath_name)
        if output_filepath_url:
            # 构建本地可访问的URL
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "PPT generated successfully", "ppt_url": output_filepath_url}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate PPT."
            )
    except Exception as e:
        logger.error(f"An unexpected error occurred during PPT generation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal server error occurred: {str(e)}"
        )


# 可选：根路径，用于测试API是否运行
@app.get("/", summary="Root endpoint")
async def root():
    return {"message": "Welcome to the PPT Generation API. Go to /docs for API documentation."}

if __name__ == '__main__':
    # 对外可以访问的IP，方便下载图片
    OUTER_IP = "http://127.0.0.1:10021"
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10021)