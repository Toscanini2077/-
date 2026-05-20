import sys
import os

# --- 核心路徑魔法 ---
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_core_dir = os.path.join(os.path.dirname(current_dir), "repo_core")
if repo_core_dir not in sys.path:
    sys.path.insert(0, repo_core_dir)
# -----------------------------------------------------------

from common import GetLi, GetShiChen, DiZHiList
from shipan.shipan import ShiPan, MinGPan
from opencc import OpenCC

def generate_shipan(req_data) -> str:
    # 1. 取得曆法數據
    li_data = GetLi(
        req_data.year, req_data.month, req_data.day, 
        req_data.hour, req_data.minute, req_data.second
    )
    
    # 🔴【修正這裡】：將月將物件轉換為純字串 ("子", "丑"...)
    yuejiang_obj = li_data[4] 
    yuejiang_str = DiZHiList[yuejiang_obj.num - 1]
    
    # 🔴【修正這裡】：計算占時並轉換為純字串
    zhanshi_obj = GetShiChen(req_data.hour)
    zhanshi_str = DiZHiList[zhanshi_obj.num - 1]
    
    # 3. 起課 (傳入的是字串 yuejiang_str 與 zhanshi_str)
    if req_data.is_mingpan:
        sq = MinGPan(
            req_data.year, req_data.month, req_data.day, 
            req_data.hour, req_data.minute, req_data.second, 
            yuejiang_str, zhanshi_str, req_data.is_daytime,
            req_data.query_matter, req_data.gender, req_data.birth_year
        )
    else:
        sq = ShiPan(
            req_data.year, req_data.month, req_data.day, 
            req_data.hour, req_data.minute, req_data.second, 
            yuejiang_str, zhanshi_str, req_data.is_daytime,
            req_data.query_matter, req_data.gender, req_data.birth_year
        )
    
    # 4. 繁簡轉換與術語修正
    cc = OpenCC('s2t')
    html_content = cc.convert(sq.toHml)
    html_content = html_content.replace('後', '后')
    html_content = html_content.replace('佔', '占')
    html_content = html_content.replace('醜', '丑')
    
    return html_content