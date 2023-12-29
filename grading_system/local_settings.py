import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
#Media 
# Add or modify the MEDIA_URL and MEDIA_ROOT settings


# Define the media root directory where uploaded files will be stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Define the URL prefix used to serve media files
MEDIA_URL = '/media/'