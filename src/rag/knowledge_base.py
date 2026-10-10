"""RAG 知识库 — 文旅数据加载"""
import json, os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def load_all_data():
    """加载所有文旅数据"""
    data = {"scenic_spots": [], "restaurants": [], "transport": [], "tips": []}
    for key, fname in [("scenic_spots", "scenic_spots.json"), ("restaurants", "restaurants.json"),
                       ("transport", "transport.json"), ("tips", "travel_tips.json")]:
        path = os.path.join(DATA_DIR, fname)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data[key] = json.load(f)
    return data
