import openai
import requests
from bs4 import BeautifulSoup
import re
import subprocess
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def fetch_job_keywords(job_url):
    # Fetch the job description from the URL
    response = requests.get(job_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_description = soup.get_text()

    # Use OpenAI API to extract keywords
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Extract key skills and requirements from the following job description."},
            {"role": "user", "content": job_description}
        ]
    )
    keywords = response.choices[0].message['content'].strip()
    return keywords

def read_original_tex(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Extract work experience section
    work_experience_match = re.search(r'\\section{Work Experience}(.+?)\\section', content, re.DOTALL)
    work_experience = work_experience_match.group(1) if work_experience_match else ""

    # Extract projects section
    projects_match = re.search(r'\\section{Projects}(.+?)(\\section|\\end{document})', content, re.DOTALL)
    projects = projects_match.group(1) if projects_match else ""

    return work_experience, projects

def generate_modified_sections(keywords, original_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Modify the following text based on these keywords: {keywords}"},
            {"role": "user", "content": original_text}
        ]
    )
    modified_text = response.choices[0].message['content'].strip()
    return modified_text

def update_tex_file(file_path, new_work_experience, new_projects):
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace the old sections with the new ones
    content = re.sub(r'(\\section{Work Experience}(.+?)(?=\\section|\\end{document}))', 
                     rf'\\section{{Work Experience}}\n{new_work_experience}\n', 
                     content, flags=re.DOTALL)
    content = re.sub(r'(\\section{Projects}(.+?)(?=\\section|\\end{document}))', 
                     rf'\\section{{Projects}}\n{new_projects}\n', 
                     content, flags=re.DOTALL)

    with open(file_path, 'w') as file:
        file.write(content)

def compile_to_pdf(tex_file, job_title):
    # Compile the LaTeX file to PDF
    pdf_name = f"Kaiyuan_resume_{job_title}.pdf"
    subprocess.run(['pdflatex', '-output-directory', 'output', tex_file])
    return pdf_name

def main():
    # job_url = input("Enter the job post URL: ")
    keywords = fetch_job_keywords('https://www.amazon.jobs/en/jobs/2836219/software-engineer-i-ios')

    work_experience, projects = read_original_tex('original.tex')

    new_work_experience = generate_modified_sections(keywords, work_experience)
    new_projects = generate_modified_sections(keywords, projects)

    update_tex_file('original.tex', new_work_experience, new_projects)

    job_title = "Software_Engineer"  # This should be extracted from the job description
    pdf_name = compile_to_pdf('original.tex', job_title)
    print(f"Generated PDF: {pdf_name}")

if __name__ == "__main__":
    main()