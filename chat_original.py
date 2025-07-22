import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# === Load Original GPT-2 Model ===
model_name = "gpt2"  # Or use "deepseek-ai/deepseek-llm-1.3b" if you're testing DeepSeek
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

# Ensure pad_token is set correctly
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# === Chat Loop ===
while True:
    prompt = input("\nYou: ")
    if prompt.lower() in {"exit", "quit"}:
        break

    encoded = tokenizer(prompt, return_tensors="pt", padding=True)
    input_ids = encoded["input_ids"].to(device)
    attention_mask = encoded["attention_mask"].to(device)

    with torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=30,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id,
        )

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    print("Model:", response[len(prompt):].strip())