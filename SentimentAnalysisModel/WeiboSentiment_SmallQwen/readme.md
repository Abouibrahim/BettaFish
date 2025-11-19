# Fine-tuning Qwen3 Small Parameter Models for Sentiment Analysis Tasks

<img src="https://github.com/666ghj/Weibo_PublicOpinion_AnalysisSystem/blob/main/static/image/logo_Qweb3.jpg" alt="Weibo Sentiment Analysis Example" width="25%" />

## Project Background

This folder is dedicated to Weibo sentiment analysis tasks based on Alibaba's Qwen3 series models. According to the latest model evaluation results, Qwen3's small parameter models (0.6B, 4B, 8B) perform excellently on relatively simple natural language processing tasks such as topic recognition and sentiment analysis, surpassing traditional base models like BERT.

The qwen 0.6B model with a linear classifier performs better than BERT and better than qwen3 235B few-shot learning for domain-specific text classification and sequence labeling tasks. With limited computational resources, the cost-effectiveness is very high...

After conducting some related research, I believe using some of Qwen3's small parameter models in this system is a good choice.

Although these parameters are considered small in the LLM era, as an individual developer with limited computing resources, fine-tuning them is still quite challenging. Training took a full four days on a single A100 GPU, please give us a star!

## Research Question

I'm also curious about a question: For example, for Qwen3-Embedding-0.6B and Qwen3-0.6B, if I attach a classification head to the former for sentiment binary classification, and perform LoRA fine-tuning on the latter, training on the same dataset, which one performs better and what are the respective advantages?

**In most cases, using Qwen3-0.6B for LoRA fine-tuning will significantly outperform using Qwen3-Embedding-0.6B with an external classification head, but performance is not as good as directly attaching a classification head.**

Therefore, this module provides both **fine-tuning** and **embedding + classification head** versions for all parameter sizes, for you to choose from.

We present the differences and trade-offs between the two approaches through a table:

| Feature / Dimension | Method A: `Qwen3-Embedding-0.6B` + Classification Head | Method B: `Qwen3-0.6B` + LoRA Fine-tuning |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Core Concept**      | **Representation Learning**                       | **Instruction Following**                         |
| **Model Learning Approach**  | Freezes the Embedding model, only trains a very small classification head (e.g., `nn.Linear`), learning the mapping from fixed text vectors to sentiment labels. | Freezes most base model parameters, fine-tunes the model's **internal attention mechanisms and knowledge representation** through training LoRA "adapters", enabling it to learn to generate specific answers based on instructions. |
| **Performance Ceiling**      | **Lower**. The model's understanding capability is limited by the general semantic representation of `Qwen3-Embedding-0.6B`, unable to learn unique, subtle sentiment patterns specific to your dataset. | **Higher**. The model adjusts its understanding of language during fine-tuning to adapt to your specific task and data distribution, better capturing complex emotions like sarcasm and internet slang. |
| **Flexibility**        | **Low**. The model can only do one thing: output classification labels. Cannot be extended.         | **High**. The model learns a "task skill". You can easily modify instructions to have it output "positive/negative/neutral", or even "why is this positive?". |
| **Training Resource Cost**  | **Very Low**. Only needs to train a classification head of a few KB to a few MB, can be completed on a regular CPU. Minimal memory usage. | **Higher**. Although LoRA is efficient, it still requires GPU, needs to load the entire 0.6B model and LoRA parameters into memory for backpropagation. |
| **Inference Speed/Cost** | **Very Fast, Very Low**. One forward pass gets the Embedding vector, classification head computation is negligible. Very suitable for large-scale, low-latency production environments. | **Slower, Higher**. Requires autoregressive generation (word by word), even if the answer is short (e.g., "positive"), it's several orders of magnitude slower than a single forward pass. |
| **Implementation Complexity**    | **Simple**. Follows the technical paradigm from the BERT era, mature workflow, intuitive code.       | **Moderate**. Requires building instruction templates, configuring LoRA parameters, using SFTTrainer, etc., slightly more complex than the former, but well-supported by mature frameworks. |

## Usage Instructions

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Activate pytorch environment
conda activate your_environment_name
```

### Model Training

**Embedding + Classification Head Method:**
```bash
python qwen3_embedding_universal.py
# The program will prompt you to select model size (0.6B/4B/8B)
```

**LoRA Fine-tuning Method:**
```bash
python qwen3_lora_universal.py
# The program will prompt you to select model size (0.6B/4B/8B)
```

**Command Line Arguments:**
```bash
# Directly specify model
python qwen3_embedding_universal.py --model_size 0.6B
python qwen3_lora_universal.py --model_size 4B

# Custom parameters
python qwen3_embedding_universal.py --model_size 8B --epochs 10 --batch_size 16
```

### Prediction Usage

**Interactive Prediction:**
```bash
python predict_universal.py
# The program will let you select specific model and method
```

**Command Line Prediction:**
```bash
# Predict with specified model
python predict_universal.py --model_type embedding --model_size 0.6B --text "Today's weather is really nice"

# Load all models
python predict_universal.py --load_all --text "This movie is amazing"
```

### Important Notes

1. **Memory Requirements**:
   - 0.6B: Minimum 4GB memory
   - 4B: Minimum 16GB memory
   - 8B: Minimum 32GB memory

2. **Data Format**: Each line formatted as `text_content\tlabel`, label is 0 (negative) or 1 (positive)

3. **Model Selection**: First-time users are recommended to start testing with the 0.6B model

4. **Training Time**: LoRA fine-tuning takes longer than the Embedding method, GPU acceleration is recommended