from torch import nn

class FinalFER2013CNN(nn.Module):
    def __init__(self, num_classes: int = 7, dropout_p: float = 0.1):
        super().__init__()
        self.dropout_p = dropout_p

        def norm_layer(channels: int):
            # fixed to BatchNorm for the final model
            return nn.BatchNorm2d(channels)

        # Block 1: 1x48x48 -> 32x24x24
        self.block1 = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            # nn.Conv2d(3, 32, kernel_size=3, padding=1),
            norm_layer(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            norm_layer(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2)   # 48 -> 24
        )

        # Block 2: 32x24x24 -> 64x12x12
        self.block2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            norm_layer(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            norm_layer(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2)   # 24 -> 12
        )

        # Block 3: 64x12x12 -> 128x6x6
        self.block3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            norm_layer(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            norm_layer(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2)   # 12 -> 6
        )

        # Block 4: 128x6x6 -> 256x6x6 + Dropout2d
        self.block4 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            norm_layer(256),
            nn.ReLU(inplace=True),
            nn.Dropout2d(self.dropout_p)
        )

        # Global average pooling + linear head
        self.fc = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = self.block4(x)

        # global average pooling over H,W -> (B, 256)
        x = x.mean(dim=(2, 3))
        x = self.fc(x)
        return x
