# Multilingual Sentiment Analysis

This module uses HuggingFace's multilingual sentiment analysis model for sentiment analysis, supporting 22 languages.

## Model Information

- **Model Name**: tabularisai/multilingual-sentiment-analysis
- **Base Model**: distilbert-base-multilingual-cased
- **Supported Languages**: 22 languages, including:
  - Chinese (中文)
  - English
  - Español (Spanish)
  - 日本語 (Japanese)
  - 한국어 (Korean)
  - Français (French)
  - Deutsch (German)
  - Русский (Russian)
  - العربية (Arabic)
  - हिन्दी (Hindi)
  - Português (Portuguese)
  - Italiano (Italian)
  - And more...

- **Output Categories**: 5-level sentiment classification
  - Very Negative
  - Negative
  - Neutral
  - Positive
  - Very Positive

## Quick Start

1. Ensure dependencies are installed:
```bash
pip install transformers torch
```

2. Run the prediction program:
```bash
python predict.py
```

3. Enter text in any language for analysis:
```
Please enter text: I love this product!
Prediction result: Very Positive (confidence: 0.9456)
```

4. View multilingual examples:
```
Please enter text: demo
```

## Code Example

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load model
model_name = "tabularisai/multilingual-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Predict
texts = [
    "今天心情很好",  # Chinese
    "I love this!",  # English
    "¡Me encanta!"   # Spanish
]

for text in texts:
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()
    sentiment_map = {0: "Very Negative", 1: "Negative", 2: "Neutral", 3: "Positive", 4: "Very Positive"}
    print(f"{text} -> {sentiment_map[prediction]}")
```

## Key Features

- **Multilingual Support**: Automatically recognizes 22 languages without specifying the language
- **5-level Fine-grained Classification**: More detailed sentiment analysis than traditional binary classification
- **High Accuracy**: Based on advanced DistilBERT architecture
- **Local Caching**: Saved locally after first download for faster subsequent use

## Application Scenarios

- International social media monitoring
- Multilingual customer feedback analysis
- Global product review sentiment classification
- Cross-language brand sentiment tracking
- Multilingual customer service optimization
- International market research

## Model Storage

- First run will automatically download the model to the `model` folder in the current directory
- Subsequent runs will load directly from local storage without re-downloading
- Model size is approximately 135MB, first download requires network connection

## File Descriptions

- `predict.py`: Main prediction program, uses direct model invocation
- `README.md`: Usage documentation

## Important Notes

- First run will automatically download the model, requires network connection
- Model will be saved to current directory for convenient subsequent use
- Supports GPU acceleration, automatically detects available devices
- To clean up model files, delete the `model` folder
- This model is trained on synthetic data, validation is recommended for real-world applications