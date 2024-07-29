import subprocess
import requests
from zipfile import ZipFile
import os

# Replace these with your actual credentials or pass them as environment variables
NGROK_AUTH_TOKEN = os.getenv('NGROK_AUTH_TOKEN', '2jvnJltrUcoAoyI189VJ3ffbDmL_2qPcDt4jhsQ2TF6Nh9Z4x')
ROOT_PASSWORD = os.getenv('ROOT_PASSWORD', 'HTTPSIAMXD')

def install_dependencies():
    print("Updating and installing dependencies...")
    subprocess.check_call(["apt-get", "update", "-y"])
    subprocess.check_call(["apt-get", "upgrade", "-y"])
    subprocess.check_call(["apt-get", "install", "openssh-server", "wget", "unzip", "-y"])

def download_and_unzip_ngrok():
    print("Downloading and unzipping Ngrok...")
    ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip"
    r = requests.get(ngrok_url)
    with open("ngrok.zip", "wb") as f:
        f.write(r.content)
    
    with ZipFile("ngrok.zip", "r") as zip_ref:
        zip_ref.extractall(".")

def configure_ngrok_and_ssh():
    print("Configuring Ngrok and SSH...")
    # Configure Ngrok with auth token
    subprocess.check_call(["./ngrok", "config", "add-authtoken", NGROK_AUTH_TOKEN])
    
    # Writing to a script to start Ngrok and SSHD
    with open("/1.sh", "w") as script:
        script.write("#!/bin/bash\n")
        script.write("./ngrok tcp 22 &>/dev/null &\n")
        script.write("/usr/sbin/sshd -D\n")
    
    # Configuring SSH
    with open("/etc/ssh/sshd_config", "a") as sshd_config:
        sshd_config.write("\nPermitRootLogin yes\n")
        sshd_config.write("PasswordAuthentication yes\n")
    
    # Setting root password
    subprocess.check_call(["chpasswd"], input=f'root:{ROOT_PASSWORD}'.encode())

    # Making the script executable
    subprocess.check_call(["chmod", "755", "/1.sh"])

def start_ssh_service():
    print("Starting SSH service...")
    subprocess.check_call(["service", "ssh", "start"])

if __name__ == "__main__":
    install_dependencies()
    download_and_unzip_ngrok()
    configure_ngrok_and_ssh()
    start_ssh_service()
    print("Setup complete. SSH and Ngrok should be running.")
  
