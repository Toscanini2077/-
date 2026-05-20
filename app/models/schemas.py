from pydantic import BaseModel, Field
from typing import Optional

class ShiPanRequest(BaseModel):
    year: int = Field(..., ge=1920, le=2100, description="起課年份")
    month: int = Field(..., ge=1, le=12, description="起課月份")
    day: int = Field(..., ge=1, le=31, description="起課日期")
    hour: int = Field(..., ge=0, le=23, description="起課小時")
    minute: int = Field(..., ge=0, le=59, description="起課分鐘")
    second: int = Field(0, ge=0, le=59, description="起課秒數")
    
    # 專屬參數
    gender: int = Field(0, description="0: 男, 1: 女")
    birth_year: int = Field(..., ge=1920, le=2100, description="求測者出生年 (本命)")
    is_daytime: bool = Field(True, description="是否為晝占 (影響貴人順逆)")
    is_mingpan: bool = Field(False, description="是否為命局 (False為事占)")
    query_matter: str = Field("", description="占測之事 (捕捉意念)")

class ShiPanResponse(BaseModel):
    status: str
    message: str
    html_content: Optional[str] = None # 暫時回傳原repo產生的HTML
    # 這裡未來可以擴充為 JSON 格式的四課、三傳陣列，供前端自由渲染