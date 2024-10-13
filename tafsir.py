import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import os
import google.generativeai as genai

API_KEY = 'AIzaSyBWJ2gmFo8wvemRY5SDeRZcb-WYFrdBGfo'
genai.configure(api_key=API_KEY)

def fetch_tafsir(surah, ayah):
    url = f"https://quran.com/en/{surah}:{ayah}/tafsirs/en-tafsir-maarif-ul-quran"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tafsir_div = soup.find('div', class_='TafsirText_md__mJWtv')
        if tafsir_div:
            tafsir_text = tafsir_div.get_text(separator=' ').strip()
            return tafsir_text
        else:
            return "Tafsir not found."
    else:
        return "Error fetching Tafsir."

def save_to_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)  
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 10, content)  
    pdf.output(filename)

surah = int(input("Enter surah number="))
size = int(input("Enter number of ayahs in surah="))
all_tafsir_text = ""

# Fetch Tafsir for all Ayahs in the Surah
for ayah in range(1, size+1):
    tafsir_text = fetch_tafsir(surah, ayah)
    if tafsir_text not in ["Tafsir not found.", "Error fetching Tafsir."]:
        all_tafsir_text += tafsir_text + " "

if all_tafsir_text:
    pdf_filename = f'tafsir_surah_{surah}.pdf'
    save_to_pdf(all_tafsir_text, pdf_filename)
    print(f"Tafsir saved to {pdf_filename}")
    model = genai.GenerativeModel("gemini-1.5-flash")
    sample_pdf = genai.upload_file(pdf_filename)
    response = model.generate_content(["Give me a summary of this PDF file.", sample_pdf])
    print("Summary of Tafsir:")
    print(response.text)
else:
    print("No Tafsir text to summarize.")
