# 1. Initialize environment acceleration frameworks on the local T4 instance
!pip install --upgrade "unsloth[colab-new] @ git+https://github.com" -q
!pip install --upgrade "unsloth_zoo @ git+https://github.com" -q
!pip install --upgrade xformers bitsandbytes accelerate transformers -q

import base64
import json
import zipfile
import os
import torch
from IPython.display import display, HTML
from unsloth import FastVisionModel 

# 2. Securely mount the 7B Vision Model in a 4-bit footprint (~7.5 GB VRAM utilized)
print("Initializing Cloud Architecture & Frontend Metamorphic Core...")
model, tokenizer = FastVisionModel.from_pretrained(
    "unsloth/Qwen2.5-VL-7B-Instruct-bnb-4bit",
    load_in_4bit = True
)
FastVisionModel.for_inference(model)

# =====================================================================
# 🎛️ CUSTOM APP GENERATION INPUT ZONE (Type your target app requirements here)
# =====================================================================
USER_CLOUD_REQUEST = """
Create a complete multi-tier IoT telemetry system for an autonomous 2WD/4WD robot 
using the AYAI Hindavi Programming System. Generate a clean, responsive single-page 
HTML5 dashboard interface tracking coordinates, speed vectors, and battery lines. 
Also, provide a lightweight Python Flask backend API script to ingest these data packets 
and log them locally or pipe them to a signaling matrix.
"""
# =====================================================================

METAMORPHIC_CLOUD_PROMPT = f"""
You are an expert Cloud Solutions Architect and Full-Stack Software Engineer.
Your task is to generate two code assets matching this specification:
"{USER_CLOUD_REQUEST}"

Asset 1: A complete, fully functional HTML5/CSS3 frontend page code.
Asset 2: A clean Python Flask backend script to run on a cloud server instance to process incoming telemetries.

Output your response using the following strict structural marker separators:
[START_FRONTEND]
(Paste only the raw HTML code here, starting with <!DOCTYPE html> and ending with </html>)
[END_FRONTEND]
[START_BACKEND]
(Paste only the raw Python script code here starting with imports)
[END_BACKEND]

Do not use markdown code block backticks or add any conversational text before or after the markers.
"""

def compile_package_and_render_links():
    print("🧠 Coding agent is synthesizing frontend components and server instances...")
    
    messages = [{"role": "user", "content": METAMORPHIC_CLOUD_PROMPT}]
    inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")
    
    with torch.inference_mode():
        outputs = model.generate(**inputs, max_new_tokens=1800, temperature=0.25)
        
    generated_raw = tokenizer.decode(outputs, skip_special_tokens=True).split("assistant\n")[-1].strip()
    
    # 3. Extract and parse structural components cleanly out of the generation string data frames
    try:
        frontend_code = generated_raw.split("[START_FRONTEND]")[1].split("[END_FRONTEND]")[0].strip()
        backend_code = generated_raw.split("[START_BACKEND]")[1].split("[END_BACKEND]")[0].strip()
    except Exception as e:
        print("Parsing fallback engaged. Ensuring raw data falls back into standard structural strings.")
        frontend_code = "<!-- Fallback UI Framework -->\n<!DOCTYPE html><html><body><h3>Dashboard Live Canvas</h3></body></html>"
        backend_code = "# Fallback Server Framework\nfrom flask import Flask\napp = Flask(__name__)\n@app.route('/')\ndef home(): return 'OK'"

    # 4. Construct the structural directory layout tree on the transient session disk
    build_dir = "cloud_app_distribution"
    os.makedirs(f"{build_dir}/frontend", exist_ok=True)
    os.makedirs(f"{build_dir}/backend", exist_ok=True)
    os.makedirs(f"{build_dir}/cloud_config", exist_ok=True)
    
    # Write application source files
    with open(f"{build_dir}/frontend/index.html", "w") as f:
        f.write(frontend_code)
    with open(f"{build_dir}/backend/server.py", "w") as f:
        f.write(backend_code)
        
    # 5. Inject actual, complete deployment configuration automation scripts for AWS/GCP instances
    setup_sh_content = """#!/bin/bash
# 🛠️ Automated Cloud Setup Initialization Script for AWS EC2 / GCP Compute Engine Instances
# Copyright (C) 2026 Abhishek Chaudhary. AYAI Hindavi Programming System. Distributed under GPLv3.

echo "Initializing production environment pipelines..."
sudo apt-get update -y
sudo apt-get install python3-pip python3-venv git Nginx -y

# Setup microservices environment isolation barriers
python3 -m venv venv
source venv/bin/activate
pip install flask requests gunicorn

echo "Configuration deployment complete. Run 'gunicorn --bind 0.0.0.0:5000 server:app' to initialize gateway loops."
"""
    with open(f"{build_dir}/cloud_config/setup.sh", "w") as f:
        f.write(setup_sh_content)

    # 6. Compress the complete multi-tier workspace into a single system zip file container
    zip_filename = "hindavi_cloud_deployment.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(build_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, build_dir)
                zipf.write(full_path, rel_path)
                
    print(f"✅ Full-stack application package successfully compiled: {zip_filename}")
    
    # 7. Render dynamic interactive interface panel optimized for mobile browsers
    deployment_panel = HTML('''
        <div style="padding: 16px; background: #0f172a; border-radius: 12px; color: #f8fafc; font-family: sans-serif; max-width: 520px; margin: 15px auto; border: 2px solid #3b82f6;">
            <h3 style="color: #3b82f6; margin-top: 0; font-size: 18px;">🚀 Universal Cloud Deployment Center</h3>
            <p style="font-size: 13px; color: #94a3b8;">Ghonchu AI has compiled your full-stack system layout, including automated server setup layers.</p>
            
            <div style="background: #1e293b; padding: 12px; border-radius: 8px; font-size: 13px; margin-bottom: 12px; border-left: 4px solid #a855f7;">
                <strong>☁️ Free Tier Console Links:</strong><br>
                • Access <a href="https://google.com" target="_blank" style="color: #a7f3d0; font-weight: bold;">🇬 Google Cloud (GCP)</a> for permanent e2-micro hosting.<br>
                • Access <a href="https://amazon.com" target="_blank" style="color: #a7f3d0; font-weight: bold;">🍊 Amazon Web Services (AWS)</a> for 12-month EC2 micro instances.
            </div>
            
            <div style="background: #1e293b; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 4px solid #10b981;">
                <strong>📦 Deployment Roadmap:</strong><br>
                1. Spin up a Linux virtual machine on your chosen cloud provider console.<br>
                2. Upload the contents of <code>hindavi_cloud_deployment.zip</code> to your server instance.<br>
                3. Execute <code>bash setup.sh</code> inside the folder to configure your live telemetry gateway ports automatically.
            </div>
        </div>
    ''')
    display(deployment_panel)

# Launch build pipelines
compile_package_and_render_links()
