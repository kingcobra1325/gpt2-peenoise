import os
from training_data import generate_t2e_training_data, generate_t2t_training_data

generate_t2t_training_data.generate()
generate_t2e_training_data.generate()

file1 = "train_t2t.jsonl"
file2 = "train_t2e.jsonl"
output_file = "train.jsonl"

# Combine the two files into one
with open(output_file, "w", encoding="utf-8") as outfile:
    for filepath in [file1, file2]:
        with open(filepath, "r", encoding="utf-8") as infile:
            for line in infile:
                outfile.write(line)

# Delete the original files
os.remove(file1)
os.remove(file2)