from datetime import datetime

def calculate_aging_effect(created_at: datetime) -> dict:
    """
    経過時間に応じたエイジング効果を計算
    """
    days = (datetime.now() - created_at).days
    
    # 基本エフェクト
    effects = {
        "animate_opacity": ft.Animation(300, "easeOut"),
        "animate_bgcolor": ft.Animation(300, "easeOut"),
        "border_radius": 10,
        "gradient": None
    }
    
    # 経過時間によるエフェクトの変化
    if days < 7:  # 1週間未満
        effects.update({
            "opacity": 1.0,
            "bgcolor": "#424242",
        })
    elif days < 30:  # 1ヶ月未満
        effects.update({
            "opacity": 0.9,
            "bgcolor": "#323232",
            "gradient": ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#424242", "#323232"]
            )
        })
    else:  # それ以上
        effects.update({
            "opacity": 0.8,
            "bgcolor": "#212121",
            "gradient": ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#323232", "#212121"]
            )
        })
    
    return effects