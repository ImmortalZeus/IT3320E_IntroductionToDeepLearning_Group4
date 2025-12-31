import cv2
import numpy as np
import torch

def preprocess_face(face_crop):
    """
    Preprocess cropped face for CNN model.
    
    Args:
        face_crop (numpy array): Grayscale cropped face image.
    
    Returns:
        torch.Tensor: Preprocessed face tensor ready for model inference.
    """
    # Resize to 48x48
    face_resized = cv2.resize(face_crop, (48, 48))
    # face_resized_gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
    

    # Convert to grayscale only if needed
    if len(face_resized.shape) == 3:  # has 3 channels
        face_resized_gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
    else:  # already grayscale
        face_resized_gray = face_resized
    
    # Normalize pixel values
    face_normalized = face_resized_gray.astype("float32") / 255.0
    
    # Convert to tensor and add batch + channel dimensions
    face_tensor = torch.tensor(face_normalized).unsqueeze(0).unsqueeze(0)
    
    return face_tensor
