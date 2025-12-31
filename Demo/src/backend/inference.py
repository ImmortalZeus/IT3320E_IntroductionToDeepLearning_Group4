import torch

def predict_emotion(model, face_tensor):
    """
    Run inference on a preprocessed face tensor.
    
    Args:
        model (torch.nn.Module): Loaded CNN model.
        face_tensor (torch.Tensor): Preprocessed face tensor [1, 1, 48, 48].
    
    Returns:
        str: Predicted emotion label.
        list: Probabilities for each class.
    """
    emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

    # model.eval()
    with torch.no_grad():
        outputs = model(face_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        predicted_class = torch.argmax(probs, dim=1).item()
    
    return emotion_labels[predicted_class], probs.squeeze().tolist()
