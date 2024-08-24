from PIL import Image
import numpy as np
import random
import os

def swap_pixels(pixels, permutation):
    height, width, _ = pixels.shape
    flattened_pixels = pixels.reshape(-1, 3)  # Flatten to a list of pixels
    
    # Apply permutation to swap pixels
    permuted_pixels = flattened_pixels[permutation]
    
    # Reshape back to image dimensions
    return permuted_pixels.reshape(height, width, 3)

def generate_permutation(size, seed):
    indices = np.arange(size)
    random.seed(seed)
    np.random.shuffle(indices)
    return indices

def encrypt_image(input_image_path, output_image_path, key):
    # Open the image
    image = Image.open(input_image_path)
    pixels = np.array(image)
    height, width, _ = pixels.shape
    total_pixels = height * width
    
    # Generate a permutation of pixel indices
    permutation = generate_permutation(total_pixels, key)
    
    # Apply pixel swapping encryption
    encrypted_pixels = swap_pixels(pixels, permutation)
    
    # Check if the output path has a valid extension
    if not output_image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        print(f"Error: The output file path '{output_image_path}' does not have a valid image extension.")
        return
    
    # Save the encrypted image
    encrypted_image = Image.fromarray(encrypted_pixels.astype(np.uint8))
    encrypted_image.save(output_image_path)
    
    # Save permutation for decryption
    np.save('permutation.npy', permutation)
    
    print(f"Image encrypted and saved to {output_image_path}")

def decrypt_image(input_image_path, output_image_path, key):
    # Open the encrypted image
    image = Image.open(input_image_path)
    pixels = np.array(image)
    height, width, _ = pixels.shape
    total_pixels = height * width
    
    # Load the saved permutation
    if not os.path.isfile('permutation.npy'):
        print("Error: Permutation file not found. Please encrypt an image first.")
        return
    
    permutation = np.load('permutation.npy')
    
    # Generate the inverse permutation using the same key
    inverse_permutation = np.argsort(permutation)
    
    # Apply pixel swapping decryption
    decrypted_pixels = swap_pixels(pixels, inverse_permutation)
    
    # Check if the output path has a valid extension
    if not output_image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        print(f"Error: The output file path '{output_image_path}' does not have a valid image extension.")
        return
    
    # Save the decrypted image
    decrypted_image = Image.fromarray(decrypted_pixels.astype(np.uint8))
    decrypted_image.save(output_image_path)
    
    print(f"Image decrypted and saved to {output_image_path}")

def main():
    # Ask user if they want to encrypt or decrypt
    choice = input("Do you want to encrypt or decrypt an image? (enter 'encrypt' or 'decrypt'): ").strip().lower()
    
    if choice == 'encrypt':
        input_image_path = input("Enter the path to the input image: ")
        key = int(input("Enter a key (integer) for encryption: "))
        encrypted_image_path = input("Enter the path to save the encrypted image (with extension): ")

        # Check if the input image file exists
        if not os.path.isfile(input_image_path):
            print(f"Error: The file '{input_image_path}' does not exist.")
            return
        
        # Encrypt the image
        encrypt_image(input_image_path, encrypted_image_path, key)

    elif choice == 'decrypt':
        input_image_path = input("Enter the path to the encrypted image: ")
        key = int(input("Enter the key (integer) used for encryption: "))
        decrypted_image_path = input("Enter the path to save the decrypted image (with extension): ")
        
        # Check if the encrypted image file exists
        if not os.path.isfile(input_image_path):
            print(f"Error: The file '{input_image_path}' does not exist.")
            return
        
        # Decrypt the image
        decrypt_image(input_image_path, decrypted_image_path, key)
        
    else:
        print("Invalid choice. Please enter 'encrypt' or 'decrypt'.")

if __name__ == "__main__":
    main()