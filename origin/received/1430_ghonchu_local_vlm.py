# 1. Install required acceleration libraries for running 4-bit Vision Models on T4
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
from unsloth import FastVisionModel # Highly efficient memory engine for T4 VRAM

# 2. Load the Vision-Language Model in 4-bit (Uses ~7-8 GB VRAM, safely below T4 limits)
print("Loading Ghonchu Vision Brain (Qwen2.5-VL-7B 4-bit)...")
model, tokenizer = FastVisionModel.from_pretrained(
    "unsloth/Qwen2.5-VL-7B-Instruct-bnb-4bit",
    load_in_4bit = True
)
FastVisionModel.for_inference(model) # Optimize model hooks for fast generation loops

# 3. Define the Global Pedagogical System Prompt for your Robotics Course
GHONCHU_SYSTEM_PROMPT = """
You are Ghonchu AI, a patient private robotics tutor for young students. 
You are watching them build an IoT robot (2WD/4WD, ESP32/Arduino).
Analyze the image provided. Look closely at their progress.
If they are doing great, encourage them. 
If it is too dark or you cannot see a chassis/wires clearly, tell them.
Keep your answer to ONE short sentence so it can be cleanly spoken out loud.
"""

def start_ghonchu_eye_tutor():
    js_code = Javascript('''
        async function runGhonchuTutor() {
            const container = document.createElement('div');
            container.style = 'padding: 15px; background: #1e293b; border-radius: 10px; color: #f8fafc; font-family: sans-serif; max-width: 450px; margin: 10px auto; border: 2px solid #38bdf8; text-align: center;';
            
            const title = document.createElement('h3');
            title.textContent = '🤖 Ghonchu Local VLM Watching Loop';
            title.style = 'color: #38bdf8; margin-top: 0;';
            
            const status = document.createElement('p');
            status.id = 'ghonchu-status';
            status.textContent = '👀 Ghonchu is loading visual cortex...';
            status.style = 'font-size: 14px; color: #94a3b8; font-weight: bold;';

            const video = document.createElement('video');
            video.style = 'width: 100%; border-radius: 6px; background: #020617; margin-bottom: 10px;';
            video.autoplay = true;
            video.playsInline = true;

            const stopBtn = document.createElement('button');
            stopBtn.textContent = 'Stop Watching';
            stopBtn.style = 'width: 100%; padding: 12px; background: #ef4444; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;';

            container.appendChild(title);
            container.appendChild(status);
            container.appendChild(video);
            container.appendChild(stopBtn);
            document.body.appendChild(container);

            const synth = window.speechSynthesis;
            function speakFeedback(text) {
                if (synth.speaking) return;
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 1.0;
                synth.speak(utterance);
            }

            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: "environment" }
            }).catch(async (err) => {
                return await navigator.mediaDevices.getUserMedia({ video: true });
            });

            video.srcObject = stream;
            status.textContent = '🤖 Local T4 VLM Engine Ready. Show me your desk!';
            speakFeedback("Local vision system activated. I am watching your desk now.");

            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            let activeLoop = true;

            stopBtn.onclick = () => {
                activeLoop = false;
                stream.getVideoTracks().forEach(track => track.stop());
                container.remove();
                speakFeedback("Goodbye!");
            };

            while (activeLoop) {
                if (video.videoWidth > 0) {
                    // Downscale image layout slightly to minimize processing delay matrices
                    canvas.width = 448; 
                    canvas.height = (video.videoHeight / video.videoWidth) * 448;
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    
                    const frameData = canvas.toDataURL('image/jpeg', 0.7);
                    const result = await google.colab.kernel.invokeFunction('notebook.process_ghonchu_frame', [frameData], {});
                    const jsonResponse = result.data['application/json'];
                    
                    if (jsonResponse && jsonResponse.voice_instruction) {
                        status.textContent = `🤖 Ghonchu: ${jsonResponse.voice_instruction}`;
                        speakFeedback(jsonResponse.voice_instruction);
                    }
                }
                // Processing locally via 4-bit VLM takes ~1.5 to 2 seconds per inference on a T4.
                // We check every 3 seconds to stay completely safe within memory cache pipelines.
                await new Promise(r => setTimeout(r, 3000)); 
            }
        }
        runGhonchuTutor();
    ''')
    display(js_code)

def process_ghonchu_frame(base64_frame):
    try:
        header, encoded = base64_frame.split(',')
        image_bytes = base64.b64decode(encoded)
        pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")
        
        # 4. Formulate the Dynamic Context Chat Prompt targeting the local VLM layers
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": GHONCHU_SYSTEM_PROMPT},
                    {"type": "image", "image": pil_image},
                    {"type": "text", "text": "Look at my workspace. Am I holding components correctly or building the chassis frame properly? Give brief audio guidance."}
                ]
            }
        ]
        
        # Tokenize and pass variables directly to local GPU registers
        inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")
        
        with torch.inference_mode():
            outputs = model.generate(
                **inputs, 
                max_new_tokens=40, 
                temperature=0.4,
                do_sample=True
            )
            
        # Extract the textual response slice cleanly
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Parse output down to clean assistant payload content string
        voice_instruction = generated_text.split("assistant\n")[-1].strip()
        
        return google.colab.output.JSONResponse({"voice_instruction": voice_instruction})
        
    except Exception as e:
        return google.colab.output.JSONResponse({"voice_instruction": ""})

# Bind context vectors
google.colab.output.register_callback('notebook.process_ghonchu_frame', process_ghonchu_frame)

# Launch
start_ghonchu_eye_tutor()
