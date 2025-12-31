import torch
import numpy as np
import cv2
from backend.face_detection import *
from backend.inference import predict_emotion
from backend.preprocessing import preprocess_face
from backend.result_handling import handle_results
from backend.CNN_model import FinalFER2013CNN
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

# Define emotion labels
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]


# Step 0: Load model
model = FinalFER2013CNN(num_classes=7, dropout_p=0.55)
state_dict = torch.load(os.path.join(current_dir, "backend", "final_fer2013.pth"), map_location=torch.device("cuda:0"))
model.load_state_dict(state_dict)
model.eval()


app = Flask(__name__, template_folder=os.path.join(current_dir, "frontend"), static_folder=os.path.join(current_dir, "frontend"))
CORS(app)  # allow all origins by default

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    image_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    # Save temp image for detection
    temp_path = os.path.join(current_dir, "temp.jpg")
    cv2.imwrite(temp_path, img)
    
    result_datas = []
    # for func in [detect_faces_cascade, detect_faces_mtcnn, detect_faces_retinaface, detect_faces_insightface]:
    for func in [detect_faces_mtcnn]:
        try:
            faces, bboxes = func(temp_path)  # adjust detect_faces to return both
            print(f"Detected {len(faces)} face(s)")
            # if len(faces) == 0:
            #     return jsonify({"error": "No face detected"}), 400

            preprocessed = preprocess_face(faces[0])
            print(preprocessed.shape)  # should be [1, 1, 48, 48]

            emotion, probabilities = predict_emotion(model, preprocessed)
            print("Predicted Emotion:", emotion)
            print("Probabilities:", probabilities)

            _, result_data = handle_results(temp_path, [bboxes[0]], emotion, probabilities, emotion_labels, False)
            print(result_data)

            result_datas.append(result_data)
        except:
            pass
    
    if(len(result_datas) > 0):
        res = {}
        res['probabilities'] = {}
        for label in emotion_labels:
            res['probabilities'][label] = sum(e['probabilities'][label] for e in result_datas) / len(result_datas)
        res['predicted_emotion'] = max(res['probabilities'], key=res['probabilities'].get)
        res['bounding_boxes'] = result_datas[0]['bounding_boxes']
        for r in result_datas:
            if r['predicted_emotion'] == res['predicted_emotion']:
                res['bounding_boxes'] = r['bounding_boxes']
                
        res_with_status_code = {"code": 200, "message": "Done!", "data": res}
                
        return jsonify(res_with_status_code)
    else:
        res_with_status_code = {"code": 400, "message": "Predict Failed!"}
        return jsonify(res_with_status_code)


if __name__ == "__main__":
    app.run(debug=False)