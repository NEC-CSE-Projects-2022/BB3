
# Team Number – A Deep Learning Approach Using ConvNeXt-Tiny and EfficientNetV2-B0 for Multi-Fruit Quality Prediction

## Team Info
- 22471A0598 — **Kambhampati John Wesly** ( [LinkedIn](https://linkedin.com/in/xxxxxxxxxx) )
_Work Done: Led the project as team leader. Handled dataset collection, preprocessing, model design, and training using ConvNeXt-Tiny. Implemented fruit classification and grading logic, optimized accuracy, and integrated the model with the full system pipeline._

- 22471A0579 — **Bokkisam Naga Anil Kumar** ( [LinkedIn](https://www.linkedin.com/in/anilkumar-data/) )
_Work Done: Supported dataset cleaning and labeling, assisted in building and validating the transfer learning model, and worked on testing the classification and grading results to ensure system accuracy and stability._

- 22471A05D8 — **Vinnakota Manoj Kumar** ( [LinkedIn](https://linkedin.com/in/xxxxxxxxxx) )
_Work Done: Focused on setting up the environment, backend integration, and frontend connection for user interaction. Helped deploy the trained model and created interfaces for fruit image upload and grading display._

- 22471A05D4 — **Shaikthettu Sharif** ( [LinkedIn](https://linkedin.com/in/xxxxxxxxxx) )
_Work Done: Contributed to dataset organization, performance analysis, and testing. Helped with report documentation, prepared the presentation, and assisted during the final evaluation and demonstration._

---

## Abstract
Automating fruit sorting is difficult because produce
varies so much in appearance and datasets are rarely balanced.
Existing solutions tend to focus on solving each of these problems,
which affects the overall efficiency of the system.This paper
proposes a dual-stage framework based deep learning system
for the integration of these two tasks. For classification of six
fruit categories in the FruitNet dataset, a ConvNeXt-Tiny model
pretrained on ImageNet is used, and an EfficientNetV2-B0 model
that has undergone same-domain transfer learning is used for
quality level grading (good, average, poor).Standard geometric
augmentations and class-weighted loss functions are applied to
mitigate class imbalance and enhance robustness.With a solid
F1-score of 95.6%, the system proves reliable enough for real
world use on edge devices, the proposed system is superior
to the existing approaches.Mostly, the suggested modular and
lightweight architecture showcases the practicality of instant fruit
evaluation on underpowered gadgets as a first important move
for extending agricultural automation.

---

## Paper Reference (Inspiration)
👉 **Multi-Fruit Classification and Grading Using a
Same-Domain Transfer Learning Approach

  Author Names :  LAMA A. ALDAKHIL ANDAESHAHA.ALMUTAIR
  
 (https://drive.google.com/file/d/1puI_8DYmHykNBS2v9Uf_I3KqmslmUcbE/view?usp=sharing)

---

## Our Improvement Over Existing Paper
- Used a dual-stage deep learning framework combining
ConvNeXt-Tiny for fruit classification and EfficientNetV2-B0 for fruit quality grading.

- Applied same-domain transfer learning between the two models
classification features from ConvNeXt-Tiny reused for quality prediction in EfficientNetV2-B0.

- Achieved higher accuracy (99.9%) and strong F1-score (95.6%),
outperforming the reference model which used only EfficientNetV2.

- Designed the system to run smoothly on low-resource local systems (CPU-only)
without the need for GPUs or high-end infrastructure.

- Integrated advanced data augmentations — AugMix, CutMix, and MixUp —
along with class-weighted loss functions to handle dataset imbalance effectively.

- Developed a lightweight, modular architecture where classification and grading
can be trained or updated independently, improving flexibility and maintenance.

- Ensured stable convergence and efficient training using early stopping,
adaptive learning rates, and two-phase fine-tuning (frozen → unfrozen layers).

- Focused on real-world usability — capable of real-time fruit detection and grading
suitable for edge devices and agricultural automation.

- Demonstrated computational efficiency — reduced training time and memory usage
while maintaining state-of-the-art accuracy.

- Presented a complete end-to-end system from dataset preparation to deployment,
proving that the research model can be transformed into a ready-to-use application.

---

## About the Project
Give a simple explanation of:
-  What your project does :
  This project automatically classifies and grades multiple types of fruits using a deep learning model based on ConvNeXt-Tiny with a same-domain transfer learning approach. It analyzes fruit images, identifies    the fruit type, and grades it according to quality parameters such as color, texture, and shape.
-  Why it is useful : 
 Manual fruit grading is time-consuming, inconsistent, and prone to human error. This automated system helps farmers, distributors, and fruit markets ensure accurate and consistent quality grading. It increases efficiency, reduces labor costs, and improves overall productivity in the agricultural supply chain.
-  General project workflow (input → processing → model → output) 
Captured fruit images are given as input → the images are preprocessed and enhanced for better accuracy → the trained ConvNeXt-Tiny-based transfer learning model classifies the fruit type and predicts its quality grade (e.g., Grade A, B, or C) → the output displays the fruit name, grade, and confidence level on the screen for users.

---

## Dataset Used
👉 **[FruitNet: Indian Fruits Dataset with Quality](https://www.kaggle.com/datasets/shashwatwork/fruitnet-indian-fruits-dataset-with-quality)**

**Dataset Details:**
This project uses a large-scale multi-fruit image dataset hosted on Google Drive due to its size. The dataset is organized into three main subsets: Train Dataset for model training, Validation Dataset for tuning model parameters and improving performance, and Test Dataset for final evaluation.

The dataset is based on the original Fruit Image Dataset prepared for multi-fruit classification and grading research.

---

## Dependencies Used
Python, Google Colab, ConvNeXt-Tiny, TensorFlow / PyTorch, OpenCV (cv2), NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, Pillow (PIL), Glob, OS, Flask, Streamlit, and TorchVision. ...

---

## EDA & Preprocessing
- Mounted Google Drive in Colab and imported the required libraries for data handling, visualization, and preprocessing.

- Reviewed the dataset by counting the number of fruit images and class labels across train, validation, and test folders.

- Verified that each image had a proper label and removed any duplicate or irrelevant files.

- Analyzed the fruit categories (e.g., apple, banana, orange, mango, etc.) and checked their class distribution to ensure balance.

- Examined image quality, resolution, and color variations to maintain consistency for model training.

- Resized all images to a fixed dimension suitable for the ConvNeXt-Tiny model input.

- Detected and removed corrupted, blurred, or unreadable fruit images.

- Normalized and standardized image pixel values to improve learning performance.

- Applied data augmentation techniques such as rotation, flipping, and brightness adjustment to increase dataset diversity.

- Completed dataset cleaning and verification to ensure the data was well-prepared for accurate fruit classification and grading.

---

## Model Training Info
The model was developed using the ConvNeXt-Tiny architecture with a same-domain transfer learning approach to achieve efficient and accurate multi-fruit classification and grading. Training was performed on Google Colab with GPU support, using a curated dataset containing thousands of fruit images divided into training, validation, and testing sets.

Before training, the dataset was thoroughly prepared by verifying image-label pairs, removing corrupted and duplicate images, standardizing all image dimensions and formats, and ensuring balanced class distribution among different fruit categories. Various data augmentation techniques such as rotation, flipping, and brightness adjustments were applied to enhance dataset diversity and model robustness.

After configuring the ConvNeXt-Tiny-based model, transfer learning was applied using pre-trained weights to improve learning efficiency. The model was trained using the processed multi-fruit dataset and fine-tuned for grading accuracy.

Post-training, the model was validated and tested using metrics such as Accuracy, Precision, Recall, and F1-score. Evaluation plots, including confusion matrices and classification reports, were analyzed to assess performance and generalization. The best-performing weights were then exported as a finalized .pth model, ready for deployment in a real-time fruit classification and grading system with an easy-to-use interface.

---

## Model Testing / Evaluation
The model was tested after training to ensure it performs accurately under real-world conditions. Validation was carried out to measure key performance metrics such as Accuracy, Precision, Recall, and F1-score, and evaluation plots like the confusion matrix and classification report were generated to analyze the quality of fruit classification and grading.

The model was further tested on a separate test dataset to verify its ability to generalize to new and unseen fruit images. After confirming consistent and stable performance across all categories, the best-performing model weights were selected and exported as a finalized .pth file.

Finally, the system was integrated with a user interface to test real-time fruit image input, ensuring reliable classification and grading output with accurate predictions and smooth deployment performance.

---

## Results
The ConvNeXt-Tiny-based model was successfully trained on a large multi-fruit dataset and evaluated using standard performance metrics such as Accuracy, Precision, Recall, and F1-score. The results showed high classification accuracy with minimal misclassifications, proving the model’s reliability for automated fruit classification and grading.

Compared to baseline CNN and transfer learning models such as ResNet and EfficientNet, the proposed ConvNeXt-Tiny model achieved better overall performance while maintaining a lightweight and efficient architecture suitable for real-time use. Fine-tuning and data augmentation further improved grading accuracy without increasing computational cost, making the system robust and scalable.

Evaluation plots such as the confusion matrix and classification report confirmed that the model can accurately classify multiple fruit types and correctly assign quality grades under varying lighting and background conditions. Testing on unseen fruit images demonstrated strong generalization capability.

The trained model was then deployed into an interactive system where users can upload fruit images for instant classification and grading. The final application operates smoothly on a local or web-based interface, confirming its readiness for real-world agricultural quality inspection and automation applications.

---

## Limitations & Future Work
   ### Limitation 
* The model was trained on a limited fruit dataset, so performance may vary when tested on new fruit types or unseen grading conditions.

* Classification accuracy may reduce under poor lighting, background clutter, or partial fruit visibility.

* The system currently relies only on RGB image input, which may affect grading precision compared to multi-spectral or hyperspectral imaging.

* Testing was mainly performed in controlled environments, so large-scale real-world validation in farms and markets is still required.
  ### Future Work 
* Train and evaluate the model on larger and more diverse fruit datasets to enhance generalization and reliability.

* Integrate IoT-based sensors or cameras for automated real-time grading in agricultural environments.

* Apply model optimization and compression techniques to deploy the system efficiently on edge or mobile devices.

* Expand the system for multi-crop classification and disease detection to support broader agricultural automation.

* Further fine-tune the ConvNeXt-Tiny model to improve grading accuracy, especially for subtle quality differences among fruits.

---

## Deployment Info
The trained ConvNeXt-Tiny model was saved as a .pth file and deployed on a local system for real-time fruit classification and grading. When a fruit image is provided through the system interface, the model automatically identifies the fruit type and predicts its quality grade (e.g., Grade A, B, or C). The system then displays the result instantly, enabling quick and accurate fruit quality assessment for use in agricultural and industrial applications.

---
