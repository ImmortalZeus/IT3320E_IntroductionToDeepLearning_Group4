import cv2
from facenet_pytorch import MTCNN

# Initialize MTCNN detector
mtcnn = MTCNN(keep_all=True)

def detect_faces_mtcnn(image_path):
    # Read image
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    if height < 60 or width < 60:
        img = cv2.resize(img, (height * 4, width * 4), interpolation=cv2.INTER_CUBIC)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect faces
    boxes, _ = mtcnn.detect(img_rgb)

    faces = []
    bboxes = []

    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = [int(coord) for coord in box]
            roi = img[y1:y2, x1:x2]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            faces.append(gray)
            bboxes.append((x1, y1, x2 - x1, y2 - y1))

    return faces, bboxes