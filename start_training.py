import json
import time
import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm  # <--- import tqdm here

# === Config ===
MODEL_NAME = "gpt2"  # or "EleutherAI/gpt-neo-125M"
BATCH_SIZE = 8
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
                self.samples.append((prompt, completion))
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        prompt, completion = self.samples[idx]
        text = f"{prompt} {completion}"
        tokenized = self.tokenizer(
            text,
            truncation=True,
            max_length=MAX_LENGTH,
            padding="max_length",
            return_tensors="pt"
        )
        input_ids = tokenized["input_ids"].squeeze()
        attention_mask = tokenized["attention_mask"].squeeze()
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": input_ids.clone()
        }


# === Load Model and Tokenizer ===
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
print("Tokenizer loaded.")

tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(DEVICE)
print("Model loaded and moved to device.")

# === Dataset & Dataloader ===
dataset = TagalogChatDataset(DATA_PATH, tokenizer)
print(f"Dataset created with {len(dataset)} samples.")

loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
print("Dataloader created.")

# === Optimizer ===
optimizer = AdamW(model.parameters(), lr=LR)
print("Optimizer initialized.")

# === Training Loop with tqdm progress bar ===
model.train()
start_time = time.time()

for epoch in range(EPOCHS):
    total_loss = 0
    progress_bar = tqdm(loader, desc=f"Epoch {epoch + 1}/{EPOCHS}", leave=False)
    for batch in progress_bar:
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
        avg_loss = total_loss / (progress_bar.n + 1)
        progress_bar.set_postfix(loss=f"{avg_loss:.4f}")

    print(f"Epoch {epoch + 1} - Loss: {total_loss / len(loader):.4f}")

end_time = time.time()
elapsed = end_time - start_time
print(f"Training completed in {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")

# === Save fine-tuned model and tokenizer ===
save_dir = "fine_tuned_gpt2_tagalog"
model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
print(f"Model and tokenizer saved to '{save_dir}'")