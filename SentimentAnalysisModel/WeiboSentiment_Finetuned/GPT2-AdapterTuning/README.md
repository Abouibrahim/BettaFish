# Weibo Sentiment Recognition Model - GPT2-Adapter Fine-tuning

## Project Description
This is a Weibo sentiment binary classification model based on GPT2, using Adapter fine-tuning technology. Through Adapter fine-tuning, the model can adapt to sentiment analysis tasks by training only a small number of parameters, significantly reducing computational resource requirements and model size.

## Dataset
Uses the Weibo sentiment dataset (weibo_senti_100k), containing approximately 100,000 Weibo posts with sentiment annotations, with about 50,000 positive and 50,000 negative comments each. Dataset labels:
- Label 0: Negative sentiment
- Label 1: Positive sentiment

## File Structure
```
GPT2-Adpter-tuning/
├── adapter.py              # Implementation of Adapter layer
├── gpt2_adapter.py         # Adapter implementation for GPT2 model
├── train.py                # Training script
├── predict.py              # Simplified prediction script (interactive use)
├── models/                 # Locally stored pre-trained models
│   └── gpt2-chinese/       # Chinese GPT2 model and configuration
├── dataset/                # Dataset directory
│   └── weibo_senti_100k.csv  # Weibo sentiment dataset
└── best_weibo_sentiment_model.pth  # Trained best model
```

## Technical Features

1. **Parameter-Efficient Fine-tuning**: Trains only about 3% of parameters compared to full fine-tuning
2. **Maintains Model Performance**: Maintains good classification performance while training only a small number of parameters
3. **Suitable for Resource-Constrained Environments**: Small model size, fast inference speed

## Environment Requirements
- Python 3.6+
- PyTorch
- Transformers
- Pandas
- NumPy
- Scikit-learn
- Tqdm

## Usage

### Train Model
```bash
python train.py
```
The training process will automatically:
- Download and locally save the Chinese GPT2 pre-trained model
- Load the Weibo sentiment dataset
- Train the model and save the best model

### Sentiment Analysis Prediction
```bash
python predict.py
```
After running, it will enter interactive mode:
- Input the Weibo text to analyze in the console
- The system will return sentiment analysis results (positive/negative) and confidence
- Enter 'q' to exit the program

## Model Structure
- Base model: `uer/gpt2-chinese-cluecorpussmall` Chinese pre-trained model
- Model local save path: `./models/gpt2-chinese/`
- Fine-tuning by adding Adapter layers after each GPT2Block
- Freeze original GPT2 parameters, train only classifier and Adapter layer parameters

## Adapter Technology
Adapter is a parameter-efficient fine-tuning technique that achieves adaptation to downstream tasks with a small number of parameters by inserting small bottleneck layers into Transformer layers. Main features:

1. **Parameter Efficient**: Compared to full parameter fine-tuning, Adapter only needs to train a small fraction of parameters
2. **Prevents Forgetting**: Keeps original pre-trained model parameters unchanged, avoiding catastrophic forgetting
3. **Multi-Task Adaptation**: Can train different Adapters for different tasks, sharing the same base model

In this project, we add an Adapter layer after each GPT2Block. The Adapter's hidden layer size is 64, much smaller than the original model's hidden layer size (typically 768 or 1024).

## Usage Example
```
Using device: cuda
Loading model: best_weibo_sentiment_model.pth

============= Weibo Sentiment Analysis =============
Enter text for analysis (enter 'q' to quit):

Enter text: This movie is so amazing, I really love it!
Prediction result: Positive sentiment (Confidence: 0.9876)

Enter text: Poor service attitude, expensive price, not recommended at all
Prediction result: Negative sentiment (Confidence: 0.9742)
```

## Notes
- The prediction script uses local model path and does not need to download the model online
- Ensure the `models/gpt2-chinese/` directory contains model files saved from the training process
- When running train.py for the first time, it will automatically download and save the model, please ensure network connection
