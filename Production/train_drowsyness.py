import torch
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim

DATASET = r"C:\Users\USER\.cache\kagglehub\datasets\ismailnasri20\driver-drowsiness-dataset-ddd\versions\1\Driver Drowsiness Dataset (DDD)"

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

dataset = datasets.ImageFolder(
    DATASET,
    transform=transform
)

loader = DataLoader(
    dataset,
    batch_size=64,
    shuffle=True,
    num_workers=0
)

print("Classes:", dataset.classes)
print("Images:", len(dataset))

# Load pretrained ResNet18
model = models.resnet18(weights="DEFAULT")

# Freeze the ResNet feature extractor
for param in model.parameters():
    param.requires_grad = False

# Replace final layer
model.fc = nn.Linear(
    model.fc.in_features,
    len(dataset.classes)
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Using:", device)

model = model.to(device)

criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    model.fc.parameters(),
    lr=0.001
)

epochs = 2

for epoch in range(epochs):

    model.train()

    total = 0
    correct = 0
    loss_total = 0

    for images, labels in loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()
        optimizer.step()

        loss_total += loss.item()

        _, predicted = torch.max(
            outputs,
            1
        )

        total += labels.size(0)

        correct += (
            predicted == labels
        ).sum().item()

    accuracy = 100 * correct / total

    print(
        f"Epoch {epoch + 1}/{epochs} "
        f"Loss: {loss_total / len(loader):.4f} "
        f"Accuracy: {accuracy:.2f}%"
    )

torch.save(
    {
        "model": model.state_dict(),
        "classes": dataset.classes
    },
    "drowsiness_model.pth"
)

print()
print("Model saved as drowsiness_model.pth")
