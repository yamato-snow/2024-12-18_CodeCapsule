from datetime import timedelta

# エイジング効果の閾値
AGING_THRESHOLDS = {
    "WEEK": timedelta(days=7),    # 1週間
    "MONTH": timedelta(days=30),  # 1ヶ月
}

# エイジング効果の視覚設定
AGING_STYLES = {
    "NEW": {
        "opacity": 1.0,
        "bgcolor": "#424242",
    },
    "WEEK_OLD": {
        "opacity": 0.9,
        "bgcolor": "#323232",
        "gradient_colors": ["#424242", "#323232"]
    },
    "MONTH_OLD": {
        "opacity": 0.8,
        "bgcolor": "#212121",
        "gradient_colors": ["#323232", "#212121"]
    }
} 