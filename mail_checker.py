from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = Flask(__name__)
CORS(app)

MODEL_PATH = r"D:\Github\PhishMateBERT\model\phishing_deberta"
MAX_LENGTH = 512

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(device)
model.eval()


def predict_email(text: str):
    inputs = tokenizer(
        text,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    ).to(device)

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits.float(), dim=-1).squeeze()

    pred_id = int(torch.argmax(probs).item())
    label = model.config.id2label[pred_id]
    confidence = probs[pred_id].item()
    return label, confidence


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not data or not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify({"error": "Missing or empty 'text' field in JSON body"}), 400

    label, confidence = predict_email(data["text"])
    return jsonify({"prediction": label, "confidence": round(confidence, 4)})


BANNER = r"""
░█████████  ░██        ░██           ░██        ░███     ░███               ░██               
░██     ░██ ░██                      ░██        ░████   ░████               ░██               
░██     ░██ ░████████  ░██ ░███████  ░████████  ░██░██ ░██░██  ░██████   ░████████  ░███████  
░█████████  ░██    ░██ ░██░██        ░██    ░██ ░██ ░████ ░██       ░██     ░██    ░██    ░██ 
░██         ░██    ░██ ░██ ░███████  ░██    ░██ ░██  ░██  ░██  ░███████     ░██    ░█████████ 
░██         ░██    ░██ ░██       ░██ ░██    ░██ ░██       ░██ ░██   ░██     ░██    ░██        
░██         ░██    ░██ ░██ ░███████  ░██    ░██ ░██       ░██  ░█████░██     ░████  ░███████  
"""

if __name__ == "__main__":
    print(BANNER)
    app.run(host="127.0.0.1", port=5000, debug=True)
