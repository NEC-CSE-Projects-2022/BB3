
## Dataset (FruitNet)

<img width="926" height="620" alt="Screenshot 2026-02-14 142254" src="https://github.com/user-attachments/assets/876cad66-635e-467d-82a2-f9864a6d0fa0" />


- **Total images:**  14700+
- **Classes:** 6 fruit types × 3 quality categories (Good, Bad, Mixed) — 18 total classes
- **Image type:** RGB Fruit images (`.jpg`)
- **Official source:** Kaggle (FruitNet: Indian Fruits Dataset with Quality)

### Download Links

- **Kaggle (official):**
  https://www.kaggle.com/datasets/shashwatwork/fruitnet-indian-fruits-dataset-with-quality

- **Project mirror (Google Drive):** <br>
  Bad Quality_Fruits:- https://drive.google.com/drive/folders/1_2Q_buzECLZHPp1NtptZVIB-bdYJYQOl <br>
  Good Quality_Fruits:- https://drive.google.com/drive/folders/1GCckupesBgtPe9_gNtLwBN442EAs8vsj<br>
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

### Your dataset has:

#### 6 Fruit Types

* Apple

* Banana

* Guava

* Lime

* Orange

* Pomegranate

#### 3 Quality Categories

* Good

* Bad

* Mixed

👉 Total possible combinations = 18 classes (if using fruit + quality together)


## Notes

* The dataset may have class imbalance across fruit types and quality categories.

* Ensure your splits (train/, val/, test/) are created consistently and do not overlap.

* Images are RGB fruit images captured under varying lighting conditions.

* Total possible classes (if using fruit + quality together) = 18 classes
(6 fruit types × 3 quality categories).

## Acknowledgements / License
* Dataset contributor: Shashwatwork
*  Kaggle hosting + documentation:
  https://www.kaggle.com/datasets/shashwatwork/fruitnet-indian-fruits-dataset-with-quality

This repository is intended for academic and research purposes. Please refer to the official dataset page for licensing and citation requirements.

 * Classes: 6 fruit types × 3 quality categories (18 total combinations)

* Image type: RGB fruit images (.jpg)

* Official source: Kaggle (recommended)
 

