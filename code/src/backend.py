from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import numpy as np
import csv
from flask_cors import CORS
from update_sentiments import update_support_history, update_social_media_history
from main import main
from image_upload import UPLOAD_FOLDER, upload_image
from image_describe import image_transcribe

app = Flask(__name__)
CORS(app)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

INVALID_SENTIMENT_SCORE = -100


def get_last_id_from_csv(file_path: str, id_column: str) -> int:
    last_id = 0
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            last_id = max(last_id, int(row[id_column].split("_")[1]))

    return last_id


@app.route("/customer_ids", methods=["GET"])
def get_customer_ids():
    df = pd.read_csv("./data/customer_profile.csv")
    return jsonify(df["customer_id"].tolist())


@app.route("/customer_profile", methods=["GET"])
def get_customer_profile():
    customer_id = request.args.get("customer_id")
    df = pd.read_csv("./data/customer_profile.csv")

    for _, row in df.iterrows():
        if row["customer_id"] == customer_id:
            try:
                if np.isnan(row["top_n_products"]):
                    row["top_n_products"] = ""
                if np.isnan(row["top_n_passive_products"]):
                    row["top_n_passive_products"] = ""
            except Exception:
                pass

            return jsonify(row.to_dict())
    return {"error": "Customer not found"}


@app.route("/customer_purchase_history", methods=["GET"])
def get_customer_purchase_history():
    customer_id = request.args.get("customer_id")
    matching_rows = []

    with open("./data/customer_purchase.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("customer_id") == customer_id:
                row["amt"] = float(row["amt"])
                matching_rows.append(row)

    return jsonify(matching_rows)


@app.route("/customer_purchase_history", methods=["POST"])
def add_customer_purchase_history():
    data = request.get_json()
    data["customer_id"] = request.args.get("customer_id")
    next_id = get_last_id_from_csv("./data/customer_purchase.csv", "transaction_id") + 1
    data["transaction_id"] = "TXN_" + str(next_id)
    with open("./data/customer_purchase.csv", mode="a", newline="") as file:
        cols = [
            "transaction_id",
            "customer_id",
            "date",
            "platform",
            "payment_method",
            "amt",
            "location",
            "item_category",
            "item_sub_category",
            "item_brand",
        ]
        writer = csv.DictWriter(file, fieldnames=cols)
        writer.writerow(data)
    return {"customer_id": data["customer_id"]}


@app.route("/customer_social_media_history", methods=["GET"])
def get_customer_social_history():
    customer_id = request.args.get("customer_id")
    matching_rows = []

    with open("./data/social_media_record.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("customer_id") == customer_id:
                row["sentiment_score"] = float(row["sentiment_score"])
                row["engagement_level"] = float(row["engagement_level"])
                matching_rows.append(row)

    return jsonify(matching_rows)


@app.route("/customer_social_media_history", methods=["POST"])
def add_customer_social_history():
    data = request.get_json()

    if "image_base64" in data:
        base64str = data["image_base64"]
        del data["image_base64"]
        upload_result = upload_image(base64str)
        if "error" in upload_result:
            return upload_result
        data["image_url"] = upload_result["url"]
        transcribed = image_transcribe(base64str)
        data["text_content"] = (
            data["text_content"].strip()
            + "\nUploaded image transcript: "
            + transcribed.strip()
        ).strip()

    next_id = get_last_id_from_csv("./data/social_media_record.csv", "post_id") + 1
    data["post_id"] = "POST_" + str(next_id)
    data["customer_id"] = request.args.get("customer_id")
    data.pop("sentiment_score", None)
    data.pop("engagement_level", None)
    data.pop("brands_liked", None)
    vals = update_social_media_history(data)
    data["sentiment_score"] = vals["sentiment_score"]
    data["engagement_level"] = vals["engagement_level"]
    data["brands_liked"] = vals["brands_liked"]
    with open("./data/social_media_record.csv", mode="a", newline="") as file:
        cols = [
            "post_id",
            "customer_id",
            "date",
            "platform",
            "image_url",
            "text_content",
            "topics_of_interest",
            "feedback_on_financial_products",
            "sentiment_score",
            "engagement_level",
            "brands_liked",
        ]
        writer = csv.DictWriter(file, fieldnames=cols)
        writer.writerow(data)
    return {"customer_id": data["customer_id"]}


@app.route("/customer_support_history", methods=["GET"])
def get_customer_support_history():
    customer_id = request.args.get("customer_id")
    matching_rows = []
    cust_sup_hist_df = pd.read_csv("./data/customer_support_record.csv")
    for index, row in cust_sup_hist_df.iterrows():
        if row[1] == customer_id:
            cust_sup_hist_dict = {}
            for cols in cust_sup_hist_df.columns:
                cust_sup_hist_dict[cols] = row[cols]
            matching_rows.append(cust_sup_hist_dict)
    return jsonify(matching_rows)


@app.route("/customer_support_history", methods=["POST"])
def add_customer_support_history():
    data = request.get_json()
    next_id = (
        get_last_id_from_csv("./data/customer_support_record.csv", "complaint_id") + 1
    )
    data["complaint_id"] = "SPRT_" + str(next_id)
    data.pop("sentiment", None)
    data["sentiment"] = update_support_history(data)
    with open("./data/customer_support_record.csv", mode="a", newline="") as file:
        cols = [
            "complaint_id",
            "customer_id",
            "date",
            "transcript",
            "main_concerns",
            "is_repeating_issue",
            "was_issue_resolved",
            "sentiment",
        ]
        writer = csv.DictWriter(file, fieldnames=cols)
        writer.writerow(data)
    return {"customer_id": data["customer_id"]}


@app.route("/customer_run_ai", methods=["POST"])
def customer_run_ai():
    data = request.get_json()
    customer_id = data.get("customer_id", "CUST_1")
    main(customer_id)
    return {"customer_id": customer_id}


@app.route("/uploads/images/<name>")
def view_image(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == "__main__":
    app.run(debug=True, port=5003)

