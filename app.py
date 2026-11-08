from flask import Flask, render_template, request
from ultralytics import YOLO
import cv2
import os
from severity import calculate_severity, calculate_priority

app = Flask(__name__)

model = YOLO("india_road_damage_best.pt")

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        file = request.files["image"]

        if file.filename == "":
            return "Please select an image"

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        results = model.predict(filepath, conf=0.25)

        result = results[0]
        output = result.plot()

        result_path = os.path.join(RESULT_FOLDER, file.filename)
        cv2.imwrite(result_path, output)

        detections = []
        severities = []

        height, width = result.orig_shape

        if result.boxes is not None:
            for box in result.boxes:
                cls = int(box.cls[0])
                confidence = float(box.conf[0])

                x1, y1, x2, y2 = box.xyxy[0].tolist()
                area = ((x2-x1) * (y2-y1)) / (width * height)

                severity = calculate_severity(area)
                severities.append(severity)

                detections.append({
                    "class": model.names[cls],
                    "confidence": round(confidence * 100, 2),
                    "severity": severity
                })

        priority = calculate_priority(severities)

        return render_template(
            "index.html",
            image=result_path,
            detections=detections,
            priority=priority
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)