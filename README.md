# 🛒 AI-ShopRecommender

AI-ShopRecommender is a modern, machine learning-based product recommendation system for e-commerce platforms. It leverages advanced ML models to provide personalized product suggestions across categories like food, fashion, and electronics.

---

## 🚀 Features
- **Personalized Recommendations** using KNN and Logistic Regression
- **Natural Language Processing** with HuggingFace Transformers
- **Image Support** for product visualization
- **Easy-to-Use GUI** built with Tkinter
- **Extensible Data** Easily add new products and categories

## 📦 Installation
1. Clone this repository:
	```bash
	git clone https://github.com/yourusername/AI-ShopRecommender.git
	cd AI-ShopRecommender
	```
2. Install dependencies:
	```bash
	pip install -r requirements.txt
	```

## 🖥️ Usage
Run the main application:
```bash
python main.py
```

## 📂 Project Structure
```
AI-ShopRecommender/
├── main.py                # Main application entry point
├── app/
│   ├── images/            # Product images
│   ├── resources/
│   │   ├── data.json      # Product and category data
│   │   └── phrases.txt    # Example product phrases
│   └── src/
│       └── ml/
│           ├── knn.py     # KNN recommendation logic
│           └── logistic_regression.py # Logistic Regression logic
└── README.md
```

## 📝 Requirements
- Python 3.8+
- TensorFlow 2.x
- HuggingFace Transformers
- Pillow
- sentence-transformers
- scikit-learn

## 📄 [Project Requirements Document](https://docs.google.com/document/d/1vHVv5BSWTqEZ3rp0qqrNEnI5iRmFwjtGEJgBIygFofU/edit?tab=t.0)

## 🙏 Credits
- [alinaduca](https://github.com/alinaduca)

---
