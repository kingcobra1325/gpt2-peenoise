import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from colorama import init

# === Initialize ANSI colors (works on Windows too) ===
init()

BLUE_BOLD   = "\033[1;34m"
YELLOW_BOLD = "\033[1;33m"
RESET       = "\033[0m"

# === Load Fine-tuned GPT-2 Model ===
save_dir = "fine_tuned_gpt2_tagalog"
tokenizer = AutoTokenizer.from_pretrained(save_dir)
model = AutoModelForCausalLM.from_pretrained(save_dir)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

# Ensure pad_token is set correctly
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# === Chat Loop ===
while True:
    # user types normally
    prompt = input("You: ")
    if prompt.lower() in {"exit", "quit"}:
        break

    # remove the plain input line (move up and clear)
    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()

    # reprint in blue-bold
    print(f"{BLUE_BOLD}You: {prompt}{RESET}")

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
    response_text = response[len(prompt):].strip()

    # model output in yellow-bold
    print(f"{YELLOW_BOLD}Model: {response_text}{RESET}")