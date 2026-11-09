# 1. Install text-to-diagram rendering dependencies
!pip install -q unsloth[colab-new] xformers bitsandbytes accelerate transformers
!apt-get install -y graphviz plantuml -q

import torch
from unsloth import FastVisionModel
from IPython.display import display, Image
import os

# 2. Configure target model (using 7B Vision variant to allow direct image validation loops)
print("Loading Architecture Intelligence Brain...")
model, tokenizer = FastVisionModel.from_pretrained(
    "unsloth/Qwen2.5-VL-7B-Instruct-bnb-4bit",
    load_in_4bit = True
)
FastVisionModel.for_inference(model)

# =====================================================================
# 📐 SYSTEMS DESIGN BOUNDARY (Define your technical target here)
# =====================================================================
SYSTEM_SPECIFICATION = """
Design a SysML Block Definition Diagram (BDD) for an autonomous CubeSat.
Include the Command & Data Handling (CDH) system, an ESP32 secondary 
communication node, the Power Management system linked to solar arrays, 
and a P2P telemetry signaling bridge out to a ground Google Sheet webhook.
"""
# =====================================================================

ARCHITECT_PROMPT = f"""
You are an expert Systems Architect and SysML/UML Modeling Engineer.
Generate a valid, clean, compileable PlantUML block configuration based on this specification:
"{SYSTEM_SPECIFICATION}"
Output ONLY the raw @startuml to @enduml block. Do not include markdown code block ticks or explanation text.
"""

# 3. Generate the declarative diagram architecture text string
messages = [{"role": "user", "content": ARCHITECT_PROMPT}]
inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")

with torch.inference_mode():
    outputs = model.generate(**inputs, max_new_tokens=400, temperature=0.2)
generated_uml = tokenizer.decode(outputs, skip_special_tokens=True).split("assistant\n")[-1].strip()

# Cleanup potential markdown wrappers introduced by the model formatting layers
clean_uml = generated_uml.replace("```plantuml", "").replace("```", "").strip()

# 4. Write string out to transient disk space and invoke system compiler
with open("system_architecture.puml", "w") as f:
    f.write(clean_uml)

print("Compiling SysML Diagram Matrix...")
os.system("plantuml system_architecture.puml")

# 5. Display visual diagram output instantly inside the student workspace
if os.path.exists("system_architecture.png"):
    display(Image("system_architecture.png"))
else:
    print("Raw Generated Modeling Text:\n", clean_uml)
