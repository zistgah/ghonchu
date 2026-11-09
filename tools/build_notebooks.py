#!/usr/bin/env python3
"""Generates notebooks/ from the cells received in origin/received, with the fixes listed in origin/SEED-DIFF.md.
Edit the received cells or this file, never the notebooks (they are regenerated).
© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.  SPDX-License-Identifier: GPL-3.0-or-later"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); REC = os.path.join(ROOT, "origin", "received")
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(ROOT, "notebooks"); os.makedirs(OUT, exist_ok=True)
COLAB = "https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/%s"
BADGE = "https://colab.research.google.com/assets/colab-badge.svg"
CR = "© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI."
LIC = "Licensed under GPL-3.0-or-later."
TM = "AyeAI® and AyeAM® are registered trade marks of Abhishek Choudhary; AyeCNSe™ (Indian TM application No. 7415871, pending)."
DROP = ("**Initial drop, 9 November 2026. Expect updates soon.** Extracted from the design discussion of the Ghonchu course "
        "(8 November 2026) and not yet run end to end; what was checked and what was changed is listed in "
        "[origin/SEED-DIFF.md](https://github.com/zistgah/ghonchu/blob/main/origin/SEED-DIFF.md).")
HOW = "Press ▶ on each step in order. Each step's code is folded behind its title; double-click a title to see it."
PRIVACY = ("**Privacy and safety.** The camera picture travels from your phone's browser to this Colab runtime, which runs on Google's "
           "cloud, not on your phone; nothing is kept unless a cell saves it. Point the camera at the robot or the object, never at a "
           "person without their informed consent; children use it with an adult, and a parent's consent comes first. Do not show "
           "patient, client or personal information. These assistants teach; they are not medical, psychological or diagnostic "
           "devices, and no prompt makes anything compliant with GDPR, HIPAA or any other law.")
FIXES = [
    ("Copyright (C) 2026 Abhishek Chaudhary. All Rights Reserved under GPLv3.", CR + " " + LIC),
    ("# Copyright (C) 2026 Abhishek Chaudhary. AYAI Hindavi Programming System. Distributed under GPLv3.", "# " + CR + " Hindawi Programming System. " + LIC),
    ("AYAI Hindavi", "AyeAI Hindawi"), ("Hindavi Programming System", "Hindawi Programming System"),
    ("Abhishek Chaudhary", "Abhishek Choudhary"), ("AYAI", "AyeAI"),
    ("stream.getVideoTracks().stop();", "stream.getVideoTracks().forEach(track => track.stop());"),
    ("b64decode(data.split(','))[1]", "b64decode(data.split(',')[1])"),
    ('!pip install --upgrade "unsloth[colab-new] @ git+https://github.com" -q\n!pip install --upgrade "unsloth_zoo @ git+https://github.com" -q\n', "!pip install -q unsloth\n"),
    ("proxy_pass http://127.0.0;", "proxy_pass http://127.0.0.1:5000;"),
    ("requests.get('https://ipify.org')", "requests.get('https://api.ipify.org')"),
    ('<a href="https://google.com" target="_blank" style="color: #a7f3d0; font-weight: bold;">🇬 Google Cloud (GCP)</a>',
     '<a href="https://console.cloud.google.com/" target="_blank" style="color: #a7f3d0; font-weight: bold;">🇬 Google Cloud (GCP)</a>'),
    ('<a href="https://amazon.com" target="_blank" style="color: #a7f3d0; font-weight: bold;">🍊 Amazon Web Services (AWS)</a>',
     '<a href="https://console.aws.amazon.com/" target="_blank" style="color: #a7f3d0; font-weight: bold;">🍊 Amazon Web Services (AWS)</a>'),
]
def fix(s):
    for a, b in FIXES:
        s = s.replace(a, b)
    if "google.colab.output.JSONResponse(" in s:  # Colab has no JSONResponse; the page reads data['application/json'], which IPython.display.JSON carries
        s = s.replace("google.colab.output.JSONResponse(", "IPython.display.JSON(").replace("import google.colab.output\n", "import google.colab.output\nimport IPython\n", 1)
    if '{"type": "image", "image": pil_image}' in s:  # Unsloth's documented vision input: an image slot in the chat, the picture passed to the processor
        s = s.replace('{"type": "image", "image": pil_image}', '{"type": "image"}')
        s = s.replace('        inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")',
                      '        input_text = tokenizer.apply_chat_template(messages, add_generation_prompt=True)\n'
                      '        inputs = tokenizer(pil_image, input_text, add_special_tokens=False, return_tensors="pt").to("cuda")')
        s = s.replace("tokenizer.decode(outputs, skip_special_tokens=True)", "tokenizer.decode(outputs[0], skip_special_tokens=True)")
    return s
def md(t): return {"cell_type": "markdown", "metadata": {}, "source": t.strip("\n")}
def code(t, title):
    t = t.strip("\n")
    if not t.startswith("#@title"): t = '#@title %s { display-mode: "form" }\n' % title + t
    return {"cell_type": "code", "metadata": {"cellView": "form"}, "execution_count": None, "outputs": [], "source": t}
def header(f, title, what, camera=False):
    cells = [md("# %s\n\n[![Open in Colab](%s)](%s)\n\n%s\n\n%s\n\n%s\n\n%s %s %s" % (title, BADGE, COLAB % f, what, DROP, HOW, CR, LIC, TM))]
    if camera: cells.append(md(PRIVACY))
    return cells
def save(f, cells, gpu=False):
    for i, c in enumerate(cells): c["id"] = "%s-%02d" % (f[:2], i)
    meta = {"colab": {"name": f, "provenance": [], "toc_visible": True}, "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}}
    if gpu: meta["accelerator"] = "GPU"
    json.dump({"nbformat": 4, "nbformat_minor": 5, "metadata": meta, "cells": cells}, open(os.path.join(OUT, f), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
def rd(n): return open(os.path.join(REC, n), encoding="utf-8").read()
def from_received_nb(n, f, title, what, camera):
    src = json.loads(rd(n)); cells = header(f, title, what, camera); last = "Step"
    for c in src["cells"]:
        s = fix("".join(c["source"]))
        if c["cell_type"] == "markdown":
            h = [l.lstrip("# ").strip() for l in s.splitlines() if l.startswith("#")]; last = h[-1] if h else last; cells.append(md(s))
        else:
            cells.append(code(s, last))
    save(f, cells)
def from_cell(n, f, title, what, step, camera=False, gpu=False, notes=None):
    cells = header(f, title, what, camera) + ([md(notes)] if notes else []) + [code(fix(rd(n)), step)]
    save(f, cells, gpu)
NB = []
def add(f, title, what): NB.append((f, title, what))
W = {}
W["00"] = "The course in one notebook: build the base in ten minutes, connect it in thirty, tune it in fifteen. Ghonchu looks at your chassis through your phone's camera."
from_received_nb("1425_master_tutor.ipynb", "00_ghonchu_master_tutor.ipynb", "Ghonchu, your robotics tutor", W["00"], True); add("00_ghonchu_master_tutor.ipynb", "Ghonchu, your robotics tutor", W["00"])
W["01"] = "Wire the motor driver to the pins in the table, then let Ghonchu look at the chassis."
from_received_nb("1426_01_chassis_and_vision.ipynb", "01_chassis_and_vision.ipynb", "Chassis and vision", W["01"], True); add("01_chassis_and_vision.ipynb", "Chassis and vision", W["01"])
W["02"] = "Register your robot on the free backbone and set the safety heartbeat that stops the motors when messages stop arriving."
from_received_nb("1426_02_network_and_telemetry.ipynb", "02_network_and_telemetry.ipynb", "Network and telemetry", W["02"], False); add("02_network_and_telemetry.ipynb", "Network and telemetry", W["02"])
W["03"] = "Ghonchu watches through the phone camera and speaks when something needs attention. This version checks the light; your own checks go into process_ghonchu_frame."
from_cell("1429_ghonchu_eye_live.py", "03_ghonchu_eye_live.ipynb", "Ghonchu's eye, live", W["03"], "Watch and speak", camera=True); add("03_ghonchu_eye_live.ipynb", "Ghonchu's eye, live", W["03"])
W["04"] = "The same eye with an open-weight vision-language model (Qwen2.5-VL 7B in 4-bit) on a Colab T4 GPU. Choose Runtime, then Change runtime type, then T4 GPU."
from_cell("1430_ghonchu_local_vlm.py", "04_ghonchu_local_vision_model.ipynb", "Ghonchu's eye with a vision model", W["04"], "Load the model, then watch and speak", camera=True, gpu=True); add("04_ghonchu_local_vision_model.ipynb", "Ghonchu's eye with a vision model", W["04"])
VAR = json.loads(rd("1431_1435_domain_variants.json"))["variants"]; base = fix(rd("1430_ghonchu_local_vlm.py"))
DOM = [("medical", "05_clinical_vision_assistant.ipynb", "Clinical vision assistant", "For clinicians and medical educators: the assistant looks at instruments, vials, labels and layouts and says one sentence about what it sees. For teaching and practice only."),
       ("epigraphy", "06_epigraphy_field_assistant.ipynb", "Epigraphy field assistant", "For historians and archaeologists: point the camera at an inscription, a coin or a sherd, and the assistant names the likely script family and what it can read. Raking light helps."),
       ("linguistics", "07_field_linguistics_assistant.ipynb", "Field linguistics assistant", "For field linguists: text, symbols and articulation described in one sentence, with IPA where it applies."),
       ("psychology", "08_psychology_observation_assistant.ipynb", "Psychology observation assistant", "For psychologists: an objective description of a room or a task set-up. It does not diagnose, and nobody is observed without informed consent."),
       ("bci", "09_bci_neuro_vision_assistant.ipynb", "BCI and neuro-vision assistant", "For BCI and neuroscience work: electrode placement, caps and signal plots, checked for plain faults such as line noise or a loose electrode. The course's robots can be driven by a NeuroSky headset.")]
for key, f, title, what in DOM:
    v = VAR[key]; s = base
    s = s.replace('GHONCHU_SYSTEM_PROMPT = """' + base.split('GHONCHU_SYSTEM_PROMPT = """')[1].split('"""')[0] + '"""', v["prompt_name"] + ' = """' + v["prompt"] + '"""')
    s = s.replace('{"type": "text", "text": GHONCHU_SYSTEM_PROMPT}', '{"type": "text", "text": %s}' % v["prompt_name"])
    s = s.replace("Look at my workspace. Am I holding components correctly or building the chassis frame properly? Give brief audio guidance.", v["ask"])
    s = s.replace("padding: 15px; background: #1e293b; border-radius: 10px; color: #f8fafc; font-family: sans-serif; max-width: 450px; margin: 10px auto; border: 2px solid #38bdf8; text-align: center;",
                  "padding: 16px; background: %s; border-radius: 12px; color: %s; font-family: sans-serif; max-width: 480px; margin: 12px auto; border: 2px solid %s; text-align: center;" % (v["bg"], v["fg"], v["accent"]))
    s = s.replace("'🤖 Ghonchu Local VLM Watching Loop'", "'%s'" % v["title"]).replace("'color: #38bdf8; margin-top: 0;'", "'color: %s; margin-top: 0; font-size: 18px;'" % v["title_color"])
    s = s.replace("'👀 Ghonchu is loading visual cortex...'", "'%s'" % v["idle"]).replace("'Stop Watching'", "'%s'" % v["stop"]).replace("background: #ef4444;", "background: %s;" % v["stop_bg"])
    s = s.replace("utterance.rate = 1.0;", "utterance.rate = %s;" % v["rate"]).replace("'🤖 Local T4 VLM Engine Ready. Show me your desk!'", "'%s'" % v["watching"])
    s = s.replace('"Local vision system activated. I am watching your desk now."', '"%s"' % v["hello"]).replace('speakFeedback("Goodbye!")', 'speakFeedback("%s")' % v["bye"])
    s = s.replace("toDataURL('image/jpeg', 0.7)", "toDataURL('image/jpeg', %s)" % v["quality"]).replace("setTimeout(r, 3000)", "setTimeout(r, %d)" % v["interval_ms"])
    s = s.replace("notebook.process_ghonchu_frame", v["callback"]).replace("`🤖 Ghonchu: ${jsonResponse.voice_instruction}`", "`%s${jsonResponse.voice_instruction}`" % v["prefix"])
    s = s.replace("max_new_tokens=40,", "max_new_tokens=%d," % v["max_new_tokens"]).replace("temperature=0.4,", "temperature=%s," % v["temperature"])
    if v["extra_pip"]: s = s.replace("!pip install --upgrade xformers bitsandbytes accelerate transformers -q", "!pip install --upgrade xformers bitsandbytes accelerate transformers %s -q" % v["extra_pip"])
    note = ("Built from the shared vision tutor with this domain's prompt, question, panel, voice and timing exactly as discussed (%s); "
            "the received cell differed from the shared one only in those, in its function names and in two panel colours, all recorded in origin/received." % v["time"])
    cells = header(f, title, what, True) + [md(note), code(s, "Load the model, then watch and speak")]; save(f, cells, True); add(f, title, what)
SPEC = [("1435_universal_metamorphic_tutor.py", "10_universal_tutor.ipynb", "One tutor for any domain", "Type the domain you are working in, and the same assistant adapts its prompt to it: robot wiring, surgical trays, Brahmi inscriptions or EEG caps.", "Choose a domain, load the model, then watch", True, True),
        ("1436_systems_architecture.py", "11_systems_architecture_sysml.ipynb", "Systems architecture in SysML", "Describe a system and get PlantUML for a SysML block definition diagram, compiled and shown in the notebook. The example is a CubeSat.", "Describe, generate and draw", False, True),
        ("1437_app_generator.py", "12_app_generator.ipynb", "An app from a sentence", "Describe a web app; the model writes a single-page app, zips it, and the notebook shows how to publish it from a phone.", "Describe, generate and package", False, True),
        ("1438_cloud_app_generator.py", "13_cloud_app_generator.ipynb", "A full stack from a sentence", "A web front end, a Flask back end and a setup script for a free-tier cloud machine, zipped together.", "Describe, generate and package", False, True),
        ("1439_beowulf_cluster.py", "14_volunteer_grid_cluster.ipynb", "Notebooks as a volunteer grid", "Nginx in front of a small Flask agent, with a shared sheet as the directory, turns many notebooks into a Beowulf-style or BOINC-style grid.", "Generate the node package", False, False),
        ("1404_stub_fill_and_zip.py", "15_stub_filling_automation.ipynb", "Filling thousands of function stubs", "For the operating-systems course: every atomic C function is specified by its interface; a loop fills each stub through an API and zips the tree. The first loop discussed is kept below as well.", "Fill the stubs and zip", False, False)]
for n, f, title, what, step, cam, gpu in SPEC:
    from_cell(n, f, title, what, step, camera=cam, gpu=gpu); add(f, title, what)
nb = json.load(open(os.path.join(OUT, "15_stub_filling_automation.ipynb"), encoding="utf-8"))
nb["cells"].append(md("The first form of the loop, with the architecture header loaded once:")); nb["cells"].append(code(fix(rd("1355_stub_fill_loop.py")), "The first loop")); save("15_stub_filling_automation.ipynb", nb["cells"])
W16 = "The environment cell for the Hindawi toolchain, the free signalling backbone on Sheets and Pages, and one tracker for every embodiment, from a toy robot to a CubeSat."
cells = header("16_backbone_and_mission_control.ipynb", "Backbone and mission control", W16) + [md("## The Hindawi environment"), code(fix(rd("1359_hindawi_init.py")), "Hindawi environment"),
         md("## The free backbone\n\nA form in front of a sheet takes each robot's registration without handing students the sheet's keys; Pages serves firmware for over-the-air updates."), code(fix(rd("1401_serverless_backbone.py")), "Register a node and publish firmware"),
         md("## One tracker for every embodiment"), code(fix(rd("1402_mission_control.py")), "Mission control")]
save("16_backbone_and_mission_control.ipynb", cells); add("16_backbone_and_mission_control.ipynb", "Backbone and mission control", W16)
W17 = "Coding agents you can run inside Colab, and the session limits to plan around."
LIM = ("## Limits to plan around\n\nAs discussed and not yet verified: a Colab session with a T4 GPU runs at most about 12 hours and stops after about 90 minutes "
       "idle, and GPU access is rationed by recent use. Work that only calls an API needs no GPU, so run it on the CPU runtime; keep files on a mounted "
       "Drive so a disconnect loses nothing. Piping a script from the internet into a shell runs whatever that address serves: read it first.")
cells = header("17_coding_agents_and_limits.ipynb", "Coding agents and Colab limits", W17) + [code(rd("1352_coding_agents.txt"), "Coding agents in a cell"), md(LIM)]
save("17_coding_agents_and_limits.ipynb", cells); add("17_coding_agents_and_limits.ipynb", "Coding agents and Colab limits", W17)
json.dump([{"file": f, "title": t, "what": w} for f, t, w in NB], open(os.path.join(OUT, "index.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("notebooks:", len(NB))
