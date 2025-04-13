from PIL import Image
import numpy as np
import base64
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# 1. Load and encode the image
def encode_image_to_text(image_path, output_text_file):
    # Load the image
    img = Image.open(image_path)
    
    # Convert to binary representation
    img_array = np.array(img)
    binary_data = img_array.tobytes()
    
    # Convert binary data to Base64
    base64_data = base64.b64encode(binary_data).decode('ascii')
    
    # Store with image metadata
    width, height = img.size
    img_format = img.format.lower()
    metadata = f"FORMAT:{img_format};WIDTH:{width};HEIGHT:{height};ENCODING:BASE64\n"
    
    # Write to text file
    with open(output_text_file, 'w') as f:
        f.write(metadata + base64_data)
    
    print(f"Image encoded and saved to {output_text_file}")
    return output_text_file

# 2. Upload the text file to Dropbox
def upload_to_dropbox(local_file_path, dropbox_path, access_token):
    try:
        # Create a Dropbox instance
        dbx = dropbox.Dropbox(access_token)
        
        # Verify the token is valid
        dbx.users_get_current_account()
        print("Successfully connected to Dropbox account")
        
        # Open the local file
        with open(local_file_path, 'rb') as f:
            file_content = f.read()
        
        # Upload the file
        print(f"Uploading {local_file_path} to Dropbox as {dropbox_path}...")
        result = dbx.files_upload(
            file_content, 
            dropbox_path, 
            mode=WriteMode('overwrite')
        )
        print(f"File successfully uploaded to {dropbox_path}")
        return result
        
    except AuthError as e:
        print(f"Authentication error: {e}")
    except ApiError as e:
        if hasattr(e.error, 'is_path') and e.error.is_path() and e.error.get_path().error.is_insufficient_space():
            print("Error: Insufficient space in Dropbox account")
        elif hasattr(e, 'user_message_text'):
            print(e.user_message_text)
        else:
            print(f"API error: {e}")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Main execution
def main():
    # Configuration
    ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN_HERE'
    image_path = 'your_image.jpg'
    text_file_path = 'image_data.txt'
    dropbox_path = '/image_data.txt'  # Must start with a forward slash
    
    # Encode image to text file
    encode_image_to_text(image_path, text_file_path)
    
    # Upload text file to Dropbox
    upload_to_dropbox(text_file_path, dropbox_path, ACCESS_TOKEN)

if name == "main":
    main()
