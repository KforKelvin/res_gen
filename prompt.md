## The goal of this project is to create a python script that generate resume based on the job description and current resume of the user.

## Design: 
- The process of the script will be the following: 
      - 1. Input 1: The script will prompt to provide the URL of the job post. Feed this URL to ChatGPT so it can fetch the key word of this job.
      - 2. Input 2: There will be a file called original.tex in the root directory. The script will fetch information from specific sections (work experience, project) of the .tex file as input. This input is the orginal copy of user's experience. 
      - 3. use ChatGPT API to generate a new, modified work experience and project section based on the keyword from the job description and the original text from the original.tex. 
      - 4. replace the work experience and project section based on generated output from the ChatGPT API. Keep the format the same (number of bulletpoint, word counts of each section) 
      - 5. Output 1: a .pdf file after modification. s