# The automation loop to pull, parse, generate, and zip thousands of files
import os
import glob
import zipfile
import google.generativeai as genai

# Setup your developer API key (Free tier supports high RPM)
genai.configure(api_key="YOUR_AI_STUDIO_API_KEY")
model = genai.GenerativeModel('gemini-2.5-flash')

# 1. Pull the student repository stubs
# !git clone https://github.com

# 2. Iterate through files and fill stubs
for filepath in glob.glob("os-spine-stubs/**/*.c", recursive=True):
    with open(filepath, "r") as f:
        content = f.read()
    
    if "// TODO: IMPLEMENT FUNCTION" in content:
        # Pass the file context directly to the API
        prompt = f"Implement the following atomic C function strictly matching its signature:\n\n{content}"
        response = model.generate_content(prompt)
        
        # Overwrite the stub file with the populated implementation
        with open(filepath, "w") as f:
            f.write(response.text)

# 3. Automatically package the fully generated workspace into a zip file
with zipfile.ZipFile('completed_kernel.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk("os-spine-stubs"):
        for file in files:
            zipf.write(os.path.join(root, file))

print("All functions processed successfully! completed_kernel.zip is ready for download.")
