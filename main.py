from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
import requests
import csv
import os

if(__name__ == '__main__'):

    # Open titles file generated from switch console
    try:
        print('[+] Fetching titles')
        with open('assets/titles.csv','r') as file_handle:

            # Create contents folder if it doesnt exist already
            if(not os.path.exists('contents')):
                os.mkdir('contents')

            # Load csv file
            reader_object = csv.DictReader(file_handle, delimiter='|')

            # Iterate through each entry
            for entry in reader_object:

                print()

                # Extract values for each entry
                title_id = entry['Title ID']
                title_name = entry['Title Name']

                print(f'[+] Processing title: {title_name}')

                # Create nested folder for title if it doesnt exist already
                if(not os.path.exists(f'contents/{title_id}')):
                    os.mkdir(f'contents/{title_id}')

                # Generate media fetch url
                title_art_url = f'https://tinfoil.media/thi/{title_id}/0/0/'

                # Start fetch request for media image
                try:
                    print(f'[+] Fetching title icon at: {title_art_url}')

                    # Create fetch request for media image
                    response = requests.get(title_art_url)

                    # Check if response checks out and write reply into file
                    if(response.status_code == 200):
                        # Save contents of request as a jpg
                        with open(f'contents/{title_id}/raw.jpg', 'wb') as image_handle:
                            image_handle.write(response.content)
                    else:
                        raise Exception(f'Unexpected response code from net request: {response.status_code}')

                except Exception as e:
                    print('[!] Error fetching title icon, Skipping...')
                    print(e)

                try:
                    print(f'[+] Processing title icon')
                    
                    # Load title image
                    raw = Image.open(fr'contents/{title_id}/raw.jpg').convert('RGB')

                    # Resize base for aspect ratio 256 x 256
                    raw = raw.resize((256, 256), Image.LANCZOS)

                    print(f'[+] Saving title icon')

                    # Save image as jpg
                    raw.save(f'contents/{title_id}/icon.jpg', 'JPEG' ,quality=100)

                    # Load title image
                    raw = Image.open(fr'contents/{title_id}/raw.jpg').convert('RGB')

                    # Resize base for aspect ratio 456 x 256
                    raw = raw.resize((456, 256), Image.LANCZOS)

                    # Save image as jpg
                    raw.save(f'contents/{title_id}/stretch.jpg', 'JPEG' ,quality=100)

                    # Delete title img
                    #os.remove(f'contents/{title_id}/raw.jpg')

                except Exception as e:
                    print('[!] Error formatting image, Skipping...')
                    print(e)
                    continue

    except Exception as e:
        print('[!] Error loading titles, Exiting...')
        print(e)
