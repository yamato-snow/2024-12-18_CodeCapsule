from datetime import datetime
import flet as ft
from config.constants import AGING_THRESHOLDS, AGING_STYLES

def calculate_aging_effect(created_at: datetime) -> dict:
    """
    経過時間に応じたエイジング効果を計算
    """
    time_passed = datetime.now() - created_at
    
    # 基本エフェクト
    effects = {
        "animate_opacity": ft.Animation(300, "easeOut"),
        "border_radius": 10,
        "gradient": None
    }
    
    # 経過時間によるエフェクトの変化
    if time_passed < AGING_THRESHOLDS["WEEK"]:  # 1週間未満
        effects.update(AGING_STYLES["NEW"])
    elif time_passed < AGING_THRESHOLDS["MONTH"]:  # 1ヶ月未満
        style = AGING_STYLES["WEEK_OLD"]
        effects.update({
            **style,
            "animate_opacity": True,
            "animation_duration": 300,
            "animation_curve": "easeOut",
            "gradient": ft.LinearGradient(
                begin=ft.Alignment.topLeft,
                end=ft.Alignment.bottomRight,
                colors=style["gradient_colors"]
            )
        })
    else:  # それ以上
        style = AGING_STYLES["MONTH_OLD"]
        effects.update({
            **style,
            "animate_opacity": True,
            "animation_duration": 300,
            "animation_curve": "easeOut",
            "gradient": ft.LinearGradient(
                begin=ft.Alignment.topLeft,
                end=ft.Alignment.bottomRight,
                colors=style["gradient_colors"]
            )
        })
    
    return effects 