import cv2
import numpy as np

def encrypt_image(image_path, key):
    # Read the image using OpenCV
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Unable to open image.")
        return

    # Scramble the image using a pseudo-random number generator based on the key
    np.random.seed(key)
    shuffle_indices = np.random.permutation(img.size)
    flat_img = img.flatten()

    # XOR the image with a random value to distort the pixel values
    encrypted_img = np.bitwise_xor(flat_img, np.random.randint(0, 256, size=flat_img.shape, dtype=np.uint8))

    # Reshape the image back to original dimensions and scramble pixel order
    encrypted_img = encrypted_img.reshape(img.shape)
    encrypted_img = encrypted_img.flatten()[shuffle_indices].reshape(img.shape)

    # Save the encrypted image
    encrypted_image_path = image_path.split('.')[0] + '_encrypted.png'
    cv2.imwrite(encrypted_image_path, encrypted_img)
    print(f"Image encrypted successfully and saved as {encrypted_image_path}")


def decrypt_image(image_path, key):
    # Read the encrypted image using OpenCV
    encrypted_img = cv2.imread(image_path)
    if encrypted_img is None:
        print("Error: Unable to open image.")
        return

    # Unscramble the image using the same pseudo-random number generator based on the key
    np.random.seed(key)
    shuffle_indices = np.random.permutation(encrypted_img.size)
    flat_img = encrypted_img.flatten()

    # Undo pixel scrambling
    original_order = np.argsort(shuffle_indices)
    unscrambled_img = flat_img[original_order].reshape(encrypted_img.shape)

    # XOR the unscrambled image with the same random values to restore original pixels
    decrypted_img = np.bitwise_xor(unscrambled_img.flatten(), np.random.randint(0, 256, size=flat_img.shape, dtype=np.uint8))

    # Reshape the image back to original dimensions
    decrypted_img = decrypted_img.reshape(encrypted_img.shape)

    # Save the decrypted image
    decrypted_image_path = image_path.split('_encrypted')[0] + '_decrypted.png'
    cv2.imwrite(decrypted_image_path, decrypted_img)
    print(f"Image decrypted successfully and saved as {decrypted_image_path}")


def main():
    image_path = input("Enter the path of the image file: ")
    key = int(input("Enter the encryption/decryption key (integer between 0 and 255): "))
    if key < 0 or key > 255:
        print("Error: Key must be between 0 and 255.")
        return

    mode = input("Enter 'e' for encryption or 'd' for decryption: ")

    if mode.lower() == 'e':
        encrypt_image(image_path, key)
    elif mode.lower() == 'd':
        decrypt_image(image_path, key)
    else:
        print("Invalid mode. Please enter 'e' for encryption or 'd' for decryption.")


if __name__ == "__main__":
    main()
