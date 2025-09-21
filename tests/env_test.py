import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("SSH_KEY_ID"))