# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Step 1: Extract links with a certain prefix
def extract_links(url, prefix):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(prefix)]
    return soup,links

# Load HTML content from a local file
def extract_links_from_local_file(file_path, prefix):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(prefix)]
    return soup,links

# Step 2: Save links to CSV file
def save_links_to_csv(links, filename):
    df = pd.DataFrame(links, columns=["Links"])
    df.to_csv(filename, index=False)

# Step 3: Visit each link and download PDFs
def download_pdfs_from_links(homepage, csv_file, download_folder):
    links_df = pd.read_csv(csv_file)
    pdf_l=[]
    for link in links_df['Links']:
        link_ = homepage + link
        response = requests.get(link_)
        soup = BeautifulSoup(response.text, 'html.parser')
        pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
                # Check if pdf_links is empty
        if not pdf_links:
            print(f"No PDF links found on page: {link}")
            continue
        
        for pdf_link in pdf_links:
            
            pdf_link = homepage+pdf_link            
            pdf_name = link.split('/')[-1] +'_'+ pdf_link.split('/')[-1]
            pdf_l.append([pdf_link,pdf_name])
            try:
                pdf_response = requests.get(pdf_link)
                pdf_response.raise_for_status()  # Check if the request was successful
                with open(os.path.join(download_folder, pdf_name), 'wb') as f:
                    f.write(pdf_response.content)
                print(f"Downloaded: {pdf_name}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {pdf_name} from {pdf_link}: {e}")
    pdf_l = pd.DataFrame(pdf_l)
    pdf_l.to_csv('pdflinks.csv')
# Define variables
url = 'annual.html'
prefix = '/publications/issues'  # Replace with your link prefix
homepage = r'https://heritage.iitm.ac.in'
csv_filename = 'links.csv'
download_folder = 'Annual Number'

# Create download folder if it doesn't exist
os.makedirs(download_folder, exist_ok=True)

# Execute functions
soup,links = extract_links_from_local_file(url, prefix)
save_links_to_csv(links, csv_filename)
download_pdfs_from_links(homepage,csv_filename, download_folder)

print("Process completed successfully.")

# %%
