import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from colorama import init

init()  # makes ANSI work nicely on Windows too

BLUE_BOLD = "\033[1;34m"
RED_BOLD  = "\033[1;31m"
RESET     = "\033[0m"

model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device).eval()
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

while True:
    # user types normally and sees what they type
    raw = input("You: ")
    if raw.lower() in {"exit", "quit"}:
        break

    # move cursor UP one line and clear it, so we can reprint in color
    sys.stdout.write("\033[F\033[K")  # up one line + clear line
    sys.stdout.flush()

    # reprint colored input
    print(f"{BLUE_BOLD}You: {raw}{RESET}")

    enc = tokenizer(raw, return_tensors="pt", padding=True)
    with torch.no_grad():
        out = model.generate(
            input_ids=enc["input_ids"].to(device),
            attention_mask=enc["attention_mask"].to(device),
            max_new_tokens=30,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id,
        )
    full = tokenizer.decode(out[0], skip_special_tokens=True)
    response_text = full[len(raw):].strip()
    print(f"{RED_BOLD}Model: {response_text}{RESET}")