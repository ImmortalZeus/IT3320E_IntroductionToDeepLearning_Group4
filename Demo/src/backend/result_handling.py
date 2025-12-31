import cv2

def handle_results(image_path, bboxes, emotion, probabilities, emotion_labels, return_image = True):
    
    if return_image:
        img = cv2.imread(image_path)

        if return_image:
            for (x, y, w, h) in bboxes:
                # Draw bounding box
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # Add emotion label
                cv2.putText(img, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 
                            0.9, (255, 0, 0), 2)

    result_data = {
        "predicted_emotion": emotion,
        "probabilities": dict(zip(emotion_labels, probabilities)),
        "bounding_boxes": [{"x": int(x), "y": int(y), "w": int(w), "h": int(h)} for (x, y, w, h) in bboxes]
    }

    return img if return_image else None, result_data
