# 1. Initialize environment acceleration frameworks on the T4 GPU runtime
!pip install --upgrade "unsloth[colab-new] @ git+https://github.com" -q
!pip install --upgrade "unsloth_zoo @ git+https://github.com" -q
!pip install --upgrade xformers bitsandbytes accelerate transformers -q

import base64
import numpy as np
import cv2
import torch
from io import BytesIO
from PIL import Image
from IPython.display import display, Javascript
import google.colab.output
from unsloth import FastVisionModel 

# 2. Securely mount the flagship 7B Vision Model in a 4-bit local footprint (~7.5 GB VRAM)
print("Initializing Metamorphic Vision Core (Local Sandbox Active)...")
model, tokenizer = FastVisionModel.from_pretrained(
    "unsloth/Qwen2.5-VL-7B-Instruct-bnb-4bit",
    load_in_4bit = True
)
FastVisionModel.for_inference(model)

# =====================================================================
# 🎛️ UNIVERSAL METAMORPHIC INTERFACE ZONE
# The researcher or student types their domain or specific task here!
# =====================================================================
TARGET_DOMAIN = "Brain-Computer Interface tracking and electrode positioning analysis" 
# Examples to type: "Robotics 2WD wiring", "Surgical instrument counting", "Brahmi script transcription"
# =====================================================================

# 3. Dynamic Meta-Prompt Factory generating targeted structural system parameters on the fly
DYNAMIC_SYSTEM_PROMPT = f"""
You are an advanced, domain-specific Physical AI Expert and Private Observation Tutor.
The user has configured this workspace session for the following explicit domain: "{TARGET_DOMAIN}".
Analyze the provided visual camera frame under strict analytical parameters matching this specified discipline.
Look closely at the environment, tools, symbols, alignments, or components related to this discipline.
Point out any anomalies, mechanical deviations, script markers, or environmental configurations.
Keep your response to ONE clear, direct sentence so it can be cleanly spoken out loud by the browser audio engine.
"""

def launch_metamorphic_vision_tutor():
    js_code = Javascript(f'''
        async function runMetamorphicTutor() {{
            const container = document.createElement('div');
            container.style = 'padding: 16px; background: #0f172a; border-radius: 12px; color: #f1f5f9; font-family: sans-serif; max-width: 480px; margin: 12px auto; border: 2px solid #10b981; text-align: center;';
            
            const title = document.createElement('h3');
            title.textContent = '🤖 Metamorphic AI Tutor Active';
            title.style = 'color: #10b981; margin-top: 0; font-size: 18px;';
            
            const status = document.createElement('p');
            status.id = 'meta-status';
            status.textContent = '🔒 Local execution loop locked onto: {TARGET_DOMAIN}';
            status.style = 'font-size: 13px; color: #94a3b8; font-style: italic;';

            const video = document.createElement('video');
            video.style = 'width: 100%; border-radius: 8px; background: #020617; margin-bottom: 12px;';
            video.autoplay = true;
            video.playsInline = true;

            const stopBtn = document.createElement('button');
            stopBtn.textContent = 'Deactivate Engine';
            stopBtn.style = 'width: 100%; padding: 12px; background: #dc2626; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;';

            container.appendChild(title);
            container.appendChild(status);
            container.appendChild(video);
            container.appendChild(stopBtn);
            document.body.appendChild(container);

            const synth = window.speechSynthesis;
            function speakFeedback(text) {{
                if (synth.speaking) return;
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 1.0; 
                synth.speak(utterance);
            }}

            const stream = await navigator.mediaDevices.getUserMedia({{
                video: {{"facingMode": "environment"}}
            }}).catch(async (err) => {{
                return await navigator.mediaDevices.getUserMedia({{ video: true }});
            }});

            video.srcObject = stream;
            status.textContent = '👀 Ghonchu AI is observing your workspace...';
            speakFeedback("Universal tutor engine active. Display your physical items or signal metrics for analysis.");

            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            let activeLoop = true;

            stopBtn.onclick = () => {{
                activeLoop = false;
                stream.getVideoTracks().forEach(track => track.stop());
                container.remove();
                speakFeedback("Observation session terminated.");
            }};

            while (activeLoop) {{
                if (video.videoWidth > 0) {{
                    canvas.width = 448; 
                    canvas.height = (video.videoHeight / video.videoWidth) * 448;
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    
                    const frameData = canvas.toDataURL(\'image/jpeg\', 0.75);
                    const result = await google.colab.kernel.invokeFunction(\'notebook.process_meta_frame\', [frameData], {{}});
                    const jsonResponse = result.data[\'application/json\'];
                    
                    if (jsonResponse && jsonResponse.voice_instruction) {{
                        status.textContent = `💡 Guidance: ${{jsonResponse.voice_instruction}}`;
                        speakFeedback(jsonResponse.voice_instruction);
                    }}
                }}
                await new Promise(r => setTimeout(r, 3500)); 
            }}
        }}
        runMetamorphicTutor();
    ''')
    display(js_code)

def process_meta_frame(base64_frame):
    try:
        header, encoded = base64_frame.split(',')
        image_bytes = base64.b64decode(encoded)
        pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")
        
        # Inject the dynamically compiled framework directly into the local execution channel
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": DYNAMIC_SYSTEM_PROMPT},
                    {"type": "image", "image": pil_image},
                    {"type": "text", "text": "Assess this active camera snapshot. Evaluate alignments, markers, or features matching the configured domain."}
                ]
            }
        ]
        
        inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")
        
        with torch.inference_mode():
            outputs = model.generate(
                **inputs, 
                max_new_tokens=45, 
                temperature=0.3, 
                do_sample=True
            )
            
        generated_text = tokenizer.decode(outputs, skip_special_tokens=True)
        voice_instruction = generated_text.split("assistant\n")[-1].strip()
        
        return google.colab.output.JSONResponse({"voice_instruction": voice_instruction})
        
    except Exception as e:
        return google.colab.output.JSONResponse({"voice_instruction": ""})

# Bind execution matrix threads
google.colab.output.register_callback('notebook.process_meta_frame', process_meta_frame)

# Start dynamic engine
launch_metamorphic_vision_tutor()
