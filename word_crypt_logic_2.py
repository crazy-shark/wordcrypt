import random
import os

VOWELS = set("AEIOU")

def is_valid_word(word):
    word = word.strip().upper()
    if not word.isalpha():
        return False
    unique_vowels = set(char for char in word if char in VOWELS)
    unique_consonants = set(char for char in word if char not in VOWELS)
    return len(unique_vowels) >= 2 and len(unique_consonants) >= 2

def load_words_from_file(filename="1500_words.txt"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)

    if not os.path.exists(file_path):
        print(f"Error: Could not find '{filename}' at {file_path}")
        return []

    valid_words = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            for word in line.replace(",", " ").split():
                clean_word = word.strip().upper()
                if is_valid_word(clean_word):
                    valid_words.append(clean_word)

    return valid_words

def apply_op(val, op_type, operand):
    if op_type == 0:
        return val + operand
    elif op_type == 1:
        return val - operand
    elif op_type == 2:
        return val * operand

def mask_number(val, op1, num1, op2, num2):
    res = apply_op(val, op1, num1)
    res = apply_op(res, op2, num2)
    return res

def generate_op_pair():
    """Generates two sequential operations ensuring op1 != op2 and operands are in range [2, 12]."""
    op1 = random.randint(0, 2)
    op2 = random.choice([op for op in range(3) if op != op1])
    num1 = random.randint(2, 12)
    num2 = random.randint(2, 12)
    return op1, num1, op2, num2

def main():
    words = load_words_from_file("1500_words.txt")
    
    if not words:
        print("No valid words found matching the constraints.")
        return

    target_word = random.choice(words)
    
    vowel_count = sum(1 for char in target_word if char in VOWELS)
    consonant_count = len(target_word) - vowel_count

    c_op1, c_num1, c_op2, c_num2 = generate_op_pair()
    v_op1, v_num1, v_op2, v_num2 = generate_op_pair()

    encrypted_numbers = []
    for char in target_word:
        base_val = ord(char) - 64
        
        if char in VOWELS:
            masked_val = mask_number(base_val, v_op1, v_num1, v_op2, v_num2)
        else:
            masked_val = mask_number(base_val, c_op1, c_num1, c_op2, c_num2)
            
        encrypted_numbers.append(str(masked_val))

    encrypted_str = ",".join(encrypted_numbers)

    print("\n----RULES----")
    print("1. Each number corresponds to a letter in the word.")
    print("2. Vowels and consonants are encrypted differently.")
    print("3. Two different sequential mathematical operations (+, -, or *) are applied to each letter's base position using operands from 2 to 12 (no consecutive identical operations).")

    print("\n--- DECODE THE WORD ---")
    print(f"Encrypted Code: {encrypted_str}")
    print(f"vowels:{vowel_count} consonants:{consonant_count}\n")

    mapping_guide = ", ".join(f"{chr(i)}:{i - 64}" for i in range(65, 91))
    print(f"Base Values: {mapping_guide}\n")

    while True:
        guess = input("Enter your guess: ").strip().upper()
        if guess == target_word:
            print("Correct! You cracked the cipher!")
            break
        else:
            print("Incorrect guess. Try again!")

if __name__ == "__main__":
    main()