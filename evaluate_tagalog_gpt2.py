import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Training with [{DEVICE.upper()}]")

# === Load the fine-tuned model and tokenizer ===
fine_tuned_dir = "fine_tuned_gpt2_tagalog"  # folder where you saved your fine-tuned model
fine_tokenizer = AutoTokenizer.from_pretrained(fine_tuned_dir)
fine_model = AutoModelForCausalLM.from_pretrained(fine_tuned_dir).to(DEVICE)
fine_model.eval()

# === Load the original GPT-2 model and tokenizer for comparison ===
original_model_name = "gpt2"
orig_tokenizer = AutoTokenizer.from_pretrained(original_model_name)
orig_tokenizer.pad_token = orig_tokenizer.eos_token
orig_model = AutoModelForCausalLM.from_pretrained(original_model_name).to(DEVICE)
orig_model.eval()

# === Load training data from train.jsonl file ===
def load_jsonl(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():  # skip empty lines
                item = json.loads(line)
                data.append(item)
    return data

training_data = load_jsonl("train.jsonl")

# Repeat or cycle data to reach 1000 prompts
num_runs = 1000
data_for_eval = (training_data * (num_runs // len(training_data) + 1))[:num_runs]

def generate_completion(model, tokenizer, prompt, max_length=50):
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length + inputs.input_ids.shape[-1],
            pad_token_id=tokenizer.pad_token_id,
            do_sample=False,  # greedy decoding for exact comparison
            eos_token_id=tokenizer.eos_token_id,
        )
    generated_text = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
    return generated_text.strip()

def evaluate_model(model, tokenizer, data):
    correct = 0
    total = len(data)

    for item in tqdm(data, desc="Evaluating"):
        prompt = item["prompt"]
        expected = item["completion"].strip()
        output = generate_completion(model, tokenizer, prompt)
        if output == expected:
            correct += 1
    
    accuracy = correct / total * 100
    return correct, total, accuracy

if __name__ == "__main__":
    print("Evaluating fine-tuned model...")
    ft_correct, ft_total, ft_acc = evaluate_model(fine_model, fine_tokenizer, data_for_eval)
    print(f"Fine-tuned GPT-2: {ft_correct}/{ft_total} correct ({ft_acc:.2f}%)")

    print("\nEvaluating original GPT-2 model...")
    orig_correct, orig_total, orig_acc = evaluate_model(orig_model, orig_tokenizer, data_for_eval)
    print(f"Original GPT-2: {orig_correct}/{orig_total} correct ({orig_acc:.2f}%)")

    print("\nSummary:")
    print(f"Fine-tuned GPT-2 improved accuracy by {ft_acc - orig_acc:.2f}% on the training-like data.")
