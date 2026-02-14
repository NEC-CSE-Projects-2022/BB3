
## Dataset (FruitNet)

<img width="926" height="620" alt="Screenshot 2026-02-14 142254" src="https://github.com/user-attachments/assets/876cad66-635e-467d-82a2-f9864a6d0fa0" />


- **Total images:**  14700+
- **Classes:** 6 fruit types × 3 quality categories (Good, Bad, Mixed) — 18 total classes
- **Image type:** RGB Fruit images (`.jpg`)
- **Official source:** Kaggle (FruitNet: Indian Fruits Dataset with Quality)

### Download Links

- **Kaggle (official):**
  https://www.kaggle.com/datasets/shashwatwork/fruitnet-indian-fruits-dataset-with-quality

- **Project mirror (Google Drive):**
  Bad Quality_Fruits:- https://drive.google.com/drive/folders/1_2Q_buzECLZHPp1NtptZVIB-bdYJYQOl
  Good Quality_Fruits:- https://drive.google.com/drive/folders/1GCckupesBgtPe9_gNtLwBN442EAs8vsj
  Mixed Quality_Fruits:- https://drive.google.com/drive/folders/16Rlz17uV_uy69pqer764bLyZwOkEMADa

> Important: Do **not** commit the dataset images to this repository.
> Download the dataset locally and place it under `Datasets/` using the structure below.

### Kaggle Download (CLI)

1. Install and configure Kaggle API credentials:
   https://github.com/Kaggle/kaggle-api#api-credentials

2. Download:
   ```bash
   kaggle datasets download -d shashwatwork/fruitnet-indian-fruits-dataset-with-quality
   ```

3. Unzip and arrange images into the structure below.

### Expected Dataset Structure

Create the following structure inside the project root:

```text
Datasets/
  train/
    Good/
      Apple/
      Banana/
      Guava/
      Lime/
      Orange/
      Pomegranate/
    Bad/
      Apple/
      Banana/
      Guava/
      Lime/
      Orange/
      Pomegranate/
    Mixed/
      Apple/
      Banana/
      Guava/
      Lime/
      Orange/
      Pomegranate/

  val/
    Good/
    Bad/
    Mixed/

  test/
    Good/
    Bad/
    Mixed/
```

This layout is compatible with **PyTorch `torchvision.datasets.ImageFolder`**.

### Class Labels

| Label | Description |
|------:|------------|
| `akiec` | Actinic keratoses and intraepithelial carcinoma |
| `bcc` | Basal cell carcinoma |
| `bkl` | Benign keratosis-like lesions |
| `df` | Dermatofibroma |
| `mel` | Melanoma |
| `nv` | Melanocytic nevi |
| `vasc` | Vascular lesions |

## Usage Example (PyTorch)

```python
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

train_dataset = ImageFolder("Datasets/train", transform=transform)
train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4
)
```

## Notes

- The dataset is known to have **strong class imbalance**.
- Ensure your splits (`train/`, `val/`, `test/`) are created consistently and do not overlap.

## Acknowledgements / License

- Dataset authors: **HAM10000 contributors**
- Kaggle hosting + documentation:
  https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000

This repository is intended for **academic and research purposes**. Please refer to the official dataset page for **licensing and citation** requirements.
 - **Classes:** 7
 - **Image type:** RGB dermoscopic images (`.jpg`)
 - **Official source:** Kaggle (recommended)
 

