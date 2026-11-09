# 1. Initialize environment acceleration frameworks on the local T4 instance
!pip install --upgrade "unsloth[colab-new] @ git+https://github.com" -q
!pip install --upgrade "unsloth_zoo @ git+https://github.com" -q
!pip install --upgrade xformers bitsandbytes accelerate transformers -q

import base64
import json
import zipfile
import os
import torch
from io import BytesIO
from PIL import Image
from IPython.display import display, Javascript, HTML
import google.colab.output
from unsloth import FastVisionModel 

# 2. Securely mount the 7B Vision Model in a 4-bit footprint (~7.5 GB VRAM utilized)
print("Initializing Metamorphic Application Intelligence Engine...")
model, tokenizer = FastVisionModel.from_pretrained(
    "unsloth/Qwen2.5-VL-7B-Instruct-bnb-4bit",
    load_in_4bit = True
)
FastVisionModel.for_inference(model)

# =====================================================================
# 🎛️ CUSTOM APP GENERATION INPUT ZONE (Type your application design target here)
# =====================================================================
USER_APP_REQUEST = """
Create a clean, dark-themed responsive single-page Dashboard Web Application for 
visualizing real-time telemetry from an autonomous 2WD/4WD Indian Robotics Platform 
using the Hindavi Programming System. Include a visual map layout placeholder box, 
numerical text cards for battery voltages and PWM speeds, and a button to send 
emergency stop command structures out to our sheets signaling database endpoint.
"""
# =====================================================================

METAMORPHIC_APP_PROMPT = f"""
You are an expert Frontend Architect and Systems Software Engineer.
Your task is to build a complete, single-file HTML5 application based strictly on this specification:
"{USER_APP_REQUEST}"

Requirements:
1. Provide a beautiful, completely functional, modern responsive CSS layout.
2. Embed all necessary UI controls, charts placeholders, and network synchronization forms internally.
3. Output ONLY the raw executable code starting with <!DOCTYPE html> and ending with </html>.
Do not wrap your answer in markdown code block ticks (```html) or print any prefix/suffix textual annotations.
"""

def compile_and_package_mobile_app():
    print("🧠 Coding agent is synthesizing application components...")
    
    messages = [{"role": "user", "content": METAMORPHIC_APP_PROMPT}]
    inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")
    
    with torch.inference_mode():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=1500, # Large target slice allocation to yield a rich UI layout
            temperature=0.3
        )
        
    generated_app = tokenizer.decode(outputs, skip_special_tokens=True).split("assistant\n")[-1].strip()
    
    # Clean potential formatting artifacts added by standard model layout generation layers
    clean_html = generated_app.replace("```html", "").replace("```", "").strip()
    
    # 3. Create structural build directories inside the transient cloud session storage disk
    os.makedirs("app_distribution/docs", exist_ok=True)
    
    # Write the core operational layout file out to disk
    html_filepath = "app_distribution/docs/index.html"
    with open(html_filepath, "w") as f:
        f.write(clean_html)
        
    # Write structural curriculum metadata out to support student review processes
    readme_content = f"# 🚀 Automated Application Package\nGenerated via AYAI Hindavi Ghonchu AI Engine.\n\n### Specifications Target Matrix:\n{USER_APP_REQUEST}"
    with open("app_distribution/README.md", "w") as f:
        f.write(readme_content)
        
    # 4. Automatically compress files down into a zip archive structure for clean cross-device handling
    zip_filename = "compiled_student_application.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk("app_distribution"):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, "app_distribution")
                zipf.write(full_path, rel_path)
                
    print(f"✅ Application packaged successfully: {zip_filename}")
    
    # 5. Inject a dynamic JavaScript interface bridge giving mobile users actionable deployment controls
    deployment_ui = HTML(f'''
        <div style="padding: 16px; background: #1e293b; border-radius: 10px; color: #f8fafc; font-family: sans-serif; max-width: 500px; margin: 15px auto; border: 2px solid #10b981;">
            <h3 style="color: #10b981; margin-top: 0;">🚀 Your Application is Ready!</h3>
            <p style="font-size: 14px; color: #94a3b8;">Ghonchu AI has compiled and zipped your serverless application dashboard code.</p>
            
            <div style="background: #0f172a; padding: 12px; border-radius: 6px; font-size: 13px; margin-bottom: 12px; border-left: 4px solid #3b82f6;">
                <strong>📲 Mobile Deployment Links:</strong><br>
                1. Open <a href="https://huggingface.co/spaces" target="_blank" style="color: #38bdf8; font-weight: bold;">🤗 Hugging Face Spaces</a> on your phone.<br>
                2. Create a space using the <strong>Static HTML SDK</strong> (completely free).<br>
                3. Go to <strong>Files and Versions</strong> and upload your <code>index.html</code> file!
            </div>
            
            <p style="font-size: 12px; color: #64748b; font-style: italic;">The system zip file container is stored at: <code>/content/{zip_filename}</code></p>
        </div>
    ''')
    display(deployment_ui)

# Execute build cycle
compile_and_package_mobile_app()
