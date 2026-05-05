from database import get_product_info


def analyze(product_name):
    data = get_product_info(product_name)

    if data:
        result = data.copy()
        result["name"] = product_name.title()
        return result

    return {
        "name": product_name.title(),
        "score": 0,
        "verdict": "NO DATA YET",
        "color": "#666666",
        "emoji": "⚪",
        "complaints": 0,
        "praises": 0,
        "bad_points": [],
        "good_points": [],
        "voices": [
            "We are still collecting enough structured public feedback for this product.",
            "Try a more common product or come back later."
        ],
        "alt_name": "",
        "alt_score": 0,
        "alt_reason": "",
        "alt_good": [],
        "alt_bad": [],
        "amazon": "",
        "flipkart": "",
        "sources": []
    }