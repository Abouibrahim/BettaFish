import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import re

def preprocess_text(text):
    return text

def main():
    print("Loading Weibo sentiment analysis model...")

    # Use HuggingFace pre-trained model
    model_name = "wsqstar/GISchat-weibo-100k-fine-tuned-bert"
    local_model_path = "./model"

    try:
        # Check if model exists locally
        import os
        if os.path.exists(local_model_path):
            print("Loading model from local storage...")
            tokenizer = AutoTokenizer.from_pretrained(local_model_path)
            model = AutoModelForSequenceClassification.from_pretrained(local_model_path)
        else:
            print("First time use, downloading model to local storage...")
            # Download and save to local
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)

            # Save to local
            tokenizer.save_pretrained(local_model_path)
            model.save_pretrained(local_model_path)
            print(f"Model saved to: {local_model_path}")

        # Set device
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)
        model.eval()
        print(f"Model loaded successfully! Using device: {device}")

    except Exception as e:
        print(f"Model loading failed: {e}")
        print("Please check network connection or use pipeline method")
        return

    print("\n============= Weibo Sentiment Analysis =============")
    print("Enter text for analysis (enter 'q' to quit):")

    while True:
        text = input("\nEnter text: ")
        if text.lower() == 'q':
            break

        if not text.strip():
            print("Input cannot be empty, please try again")
            continue

        try:
            # Preprocess text
            processed_text = preprocess_text(text)

            # Tokenize and encode
            inputs = tokenizer(
                processed_text,
                max_length=512,
                padding=True,
                truncation=True,
                return_tensors='pt'
            )

            # Move to device
            inputs = {k: v.to(device) for k, v in inputs.items()}

            # Predict
            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=1)
                prediction = torch.argmax(probabilities, dim=1).item()

            # Output results
            confidence = probabilities[0][prediction].item()
            label = "Positive sentiment" if prediction == 1 else "Negative sentiment"

            print(f"Prediction result: {label} (Confidence: {confidence:.4f})")

        except Exception as e:
            print(f"Error during prediction: {e}")
            continue

if __name__ == "__main__":
    main()