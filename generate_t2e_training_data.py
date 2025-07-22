import json
import random

# Base translation pairs (Tagalog ↔ English)
base_pairs = [
    ("Kamusta ka?", "How are you?"),
    ("Ano ang pangalan mo?", "What is your name?"),
    ("Saan ka nakatira?", "Where do you live?"),
    ("Anong ginagawa mo?", "What are you doing?"),
    ("Gusto mo ba ng kape?", "Do you want coffee?"),
    ("Ilang taon ka na?", "How old are you?"),
    ("Anong oras na?", "What time is it?"),
    ("May tanong ako.", "I have a question."),
    ("Anong trabaho mo?", "What is your job?"),
    ("Saan ka pupunta?", "Where are you going?"),
    ("Anong paborito mong pagkain?", "What is your favorite food?"),
    ("Marunong ka bang mag-Ingles?", "Do you speak English?"),
    ("Anong balita?", "What's the news?"),
    ("Taga saan ka?", "Where are you from?"),
    ("Pwede ba kitang tanungin?", "Can I ask you something?"),
    ("Mahal kita.", "I love you."),
    ("Kumain ka na ba?", "Have you eaten?"),
    ("Nasaan ka?", "Where are you?"),
    ("Ano ang ginagawa mo ngayon?", "What are you doing right now?"),
    ("Anong araw ngayon?", "What day is it today?"),
]

# Generate 5,000 samples
def generate_translation_samples(pairs, n_samples=5000):
    samples = []
    for _ in range(n_samples // 2):
        tagalog, english = random.choice(pairs)
        samples.append({"prompt": tagalog, "completion": english})
        samples.append({"prompt": english, "completion": tagalog})
    return samples

# Create the dataset
samples = generate_translation_samples(base_pairs, n_samples=5000)

# Save to JSONL file
output_file = "tagalog_english_translations_5000.jsonl"
with open(output_file, "w", encoding="utf-8") as f:
    for sample in samples:
        json.dump(sample, f, ensure_ascii=False)
        f.write("\n")

print(f"Generated {len(samples)} samples to '{output_file}'")