import os
import urllib.request
import zipfile

url = "https://mmcdnprdcontent.azureedge.net/MSDProfessionalMedicalTopics.zip"
zip_filename = "MSDProfessionalMedicalTopics.zip"
extract_dir = "MSD"
urllib.request.urlretrieve(url, zip_filename)
if not os.path.exists(extract_dir):
    os.makedirs(extract_dir)
with zipfile.ZipFile(zip_filename, "r") as zip_ref:
    zip_ref.extractall(extract_dir)
