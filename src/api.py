"""
小红书素人稿件写作 Skill - FastAPI 后端
"""

import sys
import os
import shutil

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

from skill import XiaohongshuArticleSkill

BASE_DIR = Path(__file__).parent.parent
REFERENCES_DIR = BASE_DIR / "data" / "references"
WEB_DIR = BASE_DIR / "web"

REFERENCES_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="小红书稿件生成 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_skill = XiaohongshuArticleSkill(mode="local")


class GenerateRequest(BaseModel):
    scenes: List[str]
    persona: str = "素人口吻，真实分享"
    keywords: List[str] = Field(default_factory=list)
    writing_notes: str = ""
    article_count: int = Field(default=5, ge=1, le=20)
    word_count: str = "800-1000字"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate")
def generate(req: GenerateRequest):
    result = _skill.run(
        scenes=req.scenes,
        persona=req.persona,
        keywords=req.keywords,
        writing_notes=req.writing_notes,
        article_count=req.article_count,
        word_count=req.word_count,
    )
    return result


# --- 范文管理 ---

@app.get("/references")
def list_references():
    files = [f.name for f in REFERENCES_DIR.iterdir() if f.suffix == ".docx"]
    return {"files": sorted(files)}


@app.post("/references/upload")
async def upload_reference(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="只支持 .docx 文件")
    dest = REFERENCES_DIR / file.filename
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": file.filename}


@app.delete("/references/{filename}")
def delete_reference(filename: str):
    target = REFERENCES_DIR / filename
    if not target.exists() or target.suffix != ".docx":
        raise HTTPException(status_code=404, detail="文件不存在")
    target.unlink()
    return {"deleted": filename}


# 托管前端静态文件（必须在最后挂载，避免覆盖 API 路由）
app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
