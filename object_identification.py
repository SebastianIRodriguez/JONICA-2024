import torch
import torchvision.transforms as transforms
from PIL import Image

transform = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        transforms.RandomHorizontalFlip(0.5),
        transforms.RandomRotation(40)
    ]
)

PELOTA_ROJA = 0
PELOTA_VERDE = 1
CUBO_ROJO = 2
CUBO_VERDE = 3
VACIO = 4
labels = ["PELOTA_ROJA", "PELOTA_VERDE", "CUBO_ROJO", "CUBO_VERDE", "VACIO"]

class NeuralNetwork():
    def __init__(self):
        self.model = torch.load("model.pt",map_location=torch.device("cpu"))
        self.model.eval()

    def process_image(self) -> int:
        img = Image.open("/var/www/html/img.jpg")

        x = transform(img).unsqueeze(0) # transform to tensor

        with torch.inference_mode():
            outputs = self.model(x)

        _, predictions = torch.max(outputs, 1)
        print(labels[predictions[0]])
        

        return predictions[0]
