def caesar_cipher(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def main():
    choice = input("Enter 'e' for encryption or 'd' for decryption: ")
    if choice == 'e':
        text = input("Enter text to encrypt: ")
        shift = int(input("Enter the shift value: "))
        encrypted_text = caesar_cipher(text, shift)
        print("Encrypted text:", encrypted_text)
    elif choice == 'd':
        text = input("Enter text to decrypt: ")
        shift = int(input("Enter the shift value: "))
        decrypted_text = caesar_cipher(text, -shift)
        print("Decrypted text:", decrypted_text)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
