from PIL import Image


def encrypt_image(image_path, key):
    # Open the image
    img = Image.open(image_path)
    width, height = img.size

    # Encrypt each pixel
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            encrypted_pixel = tuple((p + key) % 256 for p in pixel)  # Example: Adding the key to each pixel value
            img.putpixel((x, y), encrypted_pixel)

    # Save the encrypted image
    encrypted_image_path = image_path.split('.')[0] + '_encrypted.png'
    img.save(encrypted_image_path)
    print(f"Image encrypted successfully and saved as {encrypted_image_path}")


def decrypt_image(image_path, key):
    # Open the encrypted image
    encrypted_img = Image.open(image_path)
    width, height = encrypted_img.size

    # Decrypt each pixel
    for x in range(width):
        for y in range(height):
            pixel = encrypted_img.getpixel((x, y))
            decrypted_pixel = tuple(
                (p - key) % 256 for p in pixel)  # Example: Subtracting the key from each pixel value
            encrypted_img.putpixel((x, y), decrypted_pixel)

    # Save the decrypted image
    decrypted_image_path = image_path.split('_encrypted')[0] + '_decrypted.png'
    encrypted_img.save(decrypted_image_path)
    print(f"Image decrypted successfully and saved as {decrypted_image_path}")


def main():
    image_path = input("Enter the path of the image file: ")
    key = int(input("Enter the encryption/decryption key: "))
    mode = input("Enter 'e' for encryption or 'd' for decryption: ")

    if mode.lower() == 'e':
        encrypt_image(image_path, key)
    elif mode.lower() == 'd':
        decrypt_image(image_path, key)
    else:
        print("Invalid mode. Please enter 'e' for encryption or 'd' for decryption.")


if __name__ == "__main__":
    main()
