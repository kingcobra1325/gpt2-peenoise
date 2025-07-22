import json
import time
import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import AutoTokenizer, AutoModelForCausalLM

# === Config ===
MODEL_NAME = "gpt2"  # or "EleutherAI/gpt-neo-125M"
BATCH_SIZE = 2
EPOCHS = 5
LR = 1e-5
MAX_LENGTH = 128
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DATA_PATH = "train.jsonl"
print(f"Training with [{DEVICE.upper()}]")

# === Dataset Loader ===
class TagalogChatDataset(Dataset):
    def __init__(self, file_path, tokenizer):
        self.samples = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line)
                prompt = item["prompt"]
                completion = item["completion"]
                text = f"{prompt} {completion}"
                tokenized = tokenizer(
                    text,
                    truncation=True,
                    max_length=MAX_LENGTH,
                    padding="max_length",
                    return_tensors="pt"
                )
                input_ids = tokenized["input_ids"].squeeze()
                attention_mask = tokenized["attention_mask"].squeeze()
                self.samples.append({
                    "input_ids": input_ids,
                    "attention_mask": attention_mask,
                    "labels": input_ids.clone()
                })

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]

# === Load Model and Tokenizer ===
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(DEVICE)

# === Dataset & Dataloader ===
dataset = TagalogChatDataset(DATA_PATH, tokenizer)
print(f"Loaded {len(dataset)} training samples")
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# === Optimizer ===
optimizer = AdamW(model.parameters(), lr=LR)

# === Training Loop ===
model.train()
start_time = time.time()

for epoch in range(EPOCHS):
    total_loss = 0
    for batch in loader:
        input_ids = batch["input_ids"].to(DEVICE)
        attention_mask = batch["attention_mask"].to(DEVICE)
        labels = batch["labels"].to(DEVICE)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )

        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        total_loss += loss.item()

    print(f"Epoch {epoch + 1} - Loss: {total_loss / len(loader):.4f}")

end_time = time.time()
elapsed = end_time - start_time
print(f"Training completed in {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")

# === Save fine-tuned model and tokenizer ===
save_dir = "fine_tuned_gpt2_tagalog"
model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
print(f"Model and tokenizer saved to '{save_dir}'")
