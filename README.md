
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
👉 **[Paper Title Multi-Fruit Classification and Grading Using a
Same-Domain Transfer Learning Approach

  – Author Names LAMA A. ALDAKHIL ANDAESHAHA.ALMUTAIR
 ](https://drive.google.com/file/d/1puI_8DYmHykNBS2v9Uf_I3KqmslmUcbE/view?usp=sharing)**

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
- What your project does
  This project automatically classifies and grades multiple types of fruits using a deep learning model based on ConvNeXt-Tiny with a same-domain transfer learning approach. It analyzes fruit images, identifies    the fruit type, and grades it according to quality parameters such as color, texture, and shape.
- Why it is useful
 Manual fruit grading is time-consuming, inconsistent, and prone to human error. This automated system helps farmers, distributors, and fruit markets ensure accurate and consistent quality grading. It increases efficiency, reduces labor costs, and improves overall productivity in the agricultural supply chain.
- General project workflow (input → processing → model → output)
Captured fruit images are given as input → the images are preprocessed and enhanced for better accuracy → the trained ConvNeXt-Tiny-based transfer learning model classifies the fruit type and predicts its quality grade (e.g., Grade A, B, or C) → the output displays the fruit name, grade, and confidence level on the screen for users.

---

## Dataset Used
👉 **[Dataset Name](Dataset URL)**

**Dataset Details:**
xxxxxxxxxx

---

## Dependencies Used
xxxxxxxxxx, xxxxxxxxxx, xxxxxxxxxx ...

---

## EDA & Preprocessing
xxxxxxxxxx

---

## Model Training Info
xxxxxxxxxx

---

## Model Testing / Evaluation
xxxxxxxxxx

---

## Results
xxxxxxxxxx

---

## Limitations & Future Work
xxxxxxxxxx

---

## Deployment Info
xxxxxxxxxx

---
