import base64
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
from IPython.display import display, Javascript
import google.colab.output

def start_ghonchu_eye_tutor():
    """
    Spins up a live mobile-browser camera feed, pipes frames to Python,
    and returns real-time native browser audio feedback without blocking.
    """
    js_code = Javascript('''
        async function runGhonchuTutor() {
            // UI Container Generation
            const container = document.createElement('div');
            container.style = 'padding: 15px; background: #1e293b; border-radius: 10px; color: #f8fafc; font-family: sans-serif; max-width: 450px; margin: 10px auto; border: 2px solid #38bdf8; text-align: center;';
            
            const title = document.createElement('h3');
            title.textContent = '🤖 Ghonchu AI Active Watching Loop';
            title.style = 'color: #38bdf8; margin-top: 0;';
            
            const status = document.createElement('p');
            status.id = 'ghonchu-status';
            status.textContent = '👀 Ghonchu is scanning your desk...';
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

            // Audio Generation Configuration
            const synth = window.speechSynthesis;
            function speakFeedback(text) {
                if (synth.speaking) return; // Avoid repeating over overlapping loops
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 1.0;
                synth.speak(utterance);
            }

            // Mobile Rear Camera Interfacing Logic
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: "environment" }
            }).catch(async (err) => {
                console.log("Rear camera fallback activated.");
                return await navigator.mediaDevices.getUserMedia({ video: true });
            });

            video.srcObject = stream;
            speakFeedback("Hello! I am Ghonchu. Show me your robot chassis layout.");

            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');

            let activeLoop = true;
            stopBtn.onclick = () => {
                activeLoop = false;
                stream.getVideoTracks().forEach(track => track.stop());
                container.remove();
                speakFeedback("Good luck building!");
            };

            // Main Frame Extraction and Callback Interface Loop
            while (activeLoop) {
                if (video.videoWidth > 0) {
                    canvas.width = 240; // Kept tight to ensure instantaneous mobile transmission
                    canvas.height = (video.videoHeight / video.videoWidth) * 240;
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    
                    const frameData = canvas.toDataURL('image/jpeg', 0.6);
                    
                    // FIXED: Read the result directly from the execution wrapper promise output object
                    const result = await google.colab.kernel.invokeFunction('notebook.process_ghonchu_frame', [frameData], {});
                    const jsonResponse = result.data['application/json'];
                    
                    if (jsonResponse && jsonResponse.voice_instruction) {
                        status.textContent = `💡 Alert: ${jsonResponse.voice_instruction}`;
                        speakFeedback(jsonResponse.voice_instruction);
                    }
                }
                await new Promise(r => setTimeout(r, 1200)); // Dynamic checking pace to preserve phone temperature
            }
        }
        runGhonchuTutor();
    ''')
    display(js_code)

def process_ghonchu_frame(base64_frame):
    """
    Parses the raw mobile base64 payload layout straight into an open CV matrix
    """
    try:
        header, encoded = base64_frame.split(',')
        image_bytes = base64.b64decode(encoded)
        image = Image.open(BytesIO(image_bytes))
        cv_frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Calculate screen illumination metric levels
        avg_pixel_brightness = np.mean(cv_frame)
        voice_instruction = ""
        
        # Concrete functional example condition check:
        if avg_pixel_brightness < 40:
            voice_instruction = "Ghonchu cannot see clearly! It is too dark. Move your chassis into the light."

        # FIXED: Directly return a standard payload object back down the callback wire channel
        return google.colab.output.JSONResponse({"voice_instruction": voice_instruction})
        
    except Exception as e:
        return google.colab.output.JSONResponse({"voice_instruction": f"Error tracking frame: {str(e)}"})

# Bind callback variables inside the running notebook environment layout instance
google.colab.output.register_callback('notebook.process_ghonchu_frame', process_ghonchu_frame)

# Start execution loop
start_ghonchu_eye_tutor()
