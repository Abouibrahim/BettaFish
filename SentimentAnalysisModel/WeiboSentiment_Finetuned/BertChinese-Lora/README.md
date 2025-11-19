# Weibo Sentiment Analysis - Fine-tuned Model Based on BertChinese

This module uses a pre-trained Weibo sentiment analysis model from HuggingFace for sentiment analysis.

## Model Information

- **Model Name**: wsqstar/GISchat-weibo-100k-fine-tuned-bert
- **Model Type**: BERT Chinese sentiment classification model
- **Training Data**: 100,000 Weibo posts
- **Output**: Binary classification (positive/negative sentiment)

## Usage

### Method 1: Direct Model Invocation (Recommended)
```bash
python predict.py
```

### Method 2: Pipeline Method
```bash
python predict_pipeline.py
```

## Quick Start

1. Ensure dependencies are installed:
```bash
pip install transformers torch
```

2. Run the prediction program:
```bash
python predict.py
```

3. Enter Weibo text for analysis:
```
Enter text: The weather is great today, I feel wonderful!
Prediction result: Positive sentiment (Confidence: 0.9234)
```

## Code Example

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load model
model_name = "wsqstar/GISchat-weibo-100k-fine-tuned-bert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Predict
text = "I'm in a great mood today"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)
prediction = torch.argmax(outputs.logits, dim=1).item()
print("Positive sentiment" if prediction == 1 else "Negative sentiment")
```

## File Description

- `predict.py`: Main prediction program using direct model invocation
- `predict_pipeline.py`: Prediction program using pipeline method
- `README.md`: Usage instructions

## Model Storage

- On first run, the model will be automatically downloaded to the `model` folder in the current directory
- Subsequent runs will load directly from local storage without re-downloading
- Model size is approximately 400MB, first download requires network connection

## Notes

- First run will automatically download the model and requires network connection
- Model will be saved to current directory for future use
- Supports GPU acceleration, automatically detects available device
- To clean up model files, simply delete the `model` folder