import json
import os

import numpy as np
import requests
from requests import Response
from dotenv import load_dotenv
from numpy.lib import math


def send_request(prompt: str) -> Response:
    load_dotenv()

    OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")
    OPEN_ROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODEL = "google/gemini-2.0-flash-lite-preview-02-05:free"

    headers = {
        "Authorization": f"Bearer {OPEN_ROUTER_KEY}",
        "Content-Type": "application/json",
    }

    payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(OPEN_ROUTER_URL, headers=headers, data=json.dumps(payload))
    return response


def mahalanobis_dist(
    v1: dict[str, int], product_list: list[dict], top_n=10
) -> list[dict]:
    params = list(v1.keys())
    product_vectors = np.array([[p[k] for k in params] for p in product_list])
    X = np.array([v1[k] for k in params])

    cov = np.cov(product_vectors, rowvar=False)

    try:
        inv_cov = np.linalg.inv(cov)
    except np.linalg.LinAlgError:
        inv_cov = np.linalg.pinv(cov)

    dist = []

    for i in range(len(product_vectors)):
        distance = np.sqrt(
            np.matmul(
                np.matmul(np.transpose(X - product_vectors[i]), inv_cov),
                (X - product_vectors[i]),
            )
        )
        dist.append({"index": i, "dist": distance})

    chosen_products = sorted(dist, key=lambda d: d["dist"], reverse=False)[:top_n]
    return chosen_products


def weighted_vector_dist_passive(
    v1: dict[str, int], product_list: list[dict], weights: dict, top_n=10
) -> list[dict]:
    params = list(v1.keys())
    chosen_products = []

    for j in range(len(product_list)):
        if (v1["risk_customer"] - product_list[j]["risk_customer"]) <= -1 or (
            v1["risk_bank"] - product_list[j]["risk_bank"]
        ) <= -1:
            continue
        dist = math.sqrt(
            sum(
                [
                    weights[params[i]]
                    * math.pow((v1[params[i]] - product_list[j][params[i]]), 2)
                    for i in range(len(params))
                ]
            )
        )
        chosen_products.append({"index": j, "dist": dist})

    chosen_products = sorted(chosen_products, key=lambda d: d["dist"], reverse=False)[
        :top_n
    ]
    return chosen_products


def load_product_list(file_path: str = "./data/financial_products.json") -> list[dict]:
    product_list = []

    with open(file_path, "r") as file:
        try:
            product_list = json.load(file)
        except json.JSONDecodeError:
            return []

    return product_list
