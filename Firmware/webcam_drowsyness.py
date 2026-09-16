import cv2
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# Load trained model
checkpoint = torch.load(
    "drowsiness_model.pth",
    map_location="cpu"
)

classes = checkpoint["classes"]

model = models.resnet18(weights=None)

model.fc = nn.Linear(
    model.fc.in_features,
    len(classes)
)

model.load_state_dict(checkpoint["model"])
model.eval()

# Same preprocessing used during training
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

print("Webcam started.")
print("Press Q to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Could not read webcam frame.")
        break

    # OpenCV BGR -> RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to PIL image
    image = Image.fromarray(rgb)

    # Prepare image for model
    input_tensor = transform(image).unsqueeze(0)

    # Prediction
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.softmax(output, dim=1)[0]

    prediction = torch.argmax(probabilities).item()

    label = classes[prediction]
    confidence = probabilities[prediction].item() * 100

    text = f"{label}: {confidence:.1f}%"

    cv2.putText(
        frame,
        text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Drowsiness Detection", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
