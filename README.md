# Ghonchu

Ghonchu is the friendly tutor of Abhishek Choudhary's robotics course: Colab notebooks that run on a phone, from a child's first plastic robot to research.

**Initial drop, 9 November 2026. Expect updates soon.** The notebooks are extracted from the course's design discussion of 8 November 2026 and have not yet been run end to end. What was checked and what was changed is in [origin/SEED-DIFF.md](origin/SEED-DIFF.md).

**Abhishek Choudhary**, AyeAI. ORCID [0009-0002-0684-8320](https://orcid.org/0009-0002-0684-8320). Contact: ayeai.ayeam@gmail.com

© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.

## Meet Ghonchu

[zistgah.github.io/ghonchu](https://zistgah.github.io/ghonchu/): a round, glowing tutor who bounces, hops, blinks and follows your finger with its eyes. Tap it and it jumps and says something useful.

## The notebooks

| Open | Notebook | What it does |
|:--|:--|:--|
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/00_ghonchu_master_tutor.ipynb) | Ghonchu, your robotics tutor | The course in one notebook: build the base in ten minutes, connect it in thirty, tune it in fifteen. Ghonchu looks at your chassis through your phone's camera. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/01_chassis_and_vision.ipynb) | Chassis and vision | Wire the motor driver to the pins in the table, then let Ghonchu look at the chassis. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/02_network_and_telemetry.ipynb) | Network and telemetry | Register your robot on the free backbone and set the safety heartbeat that stops the motors when messages stop arriving. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/03_ghonchu_eye_live.ipynb) | Ghonchu's eye, live | Ghonchu watches through the phone camera and speaks when something needs attention. This version checks the light; your own checks go into process_ghonchu_frame. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/04_ghonchu_local_vision_model.ipynb) | Ghonchu's eye with a vision model | The same eye with an open-weight vision-language model (Qwen2.5-VL 7B in 4-bit) on a Colab T4 GPU. Choose Runtime, then Change runtime type, then T4 GPU. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/05_clinical_vision_assistant.ipynb) | Clinical vision assistant | For clinicians and medical educators: the assistant looks at instruments, vials, labels and layouts and says one sentence about what it sees. For teaching and practice only. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/06_epigraphy_field_assistant.ipynb) | Epigraphy field assistant | For historians and archaeologists: point the camera at an inscription, a coin or a sherd, and the assistant names the likely script family and what it can read. Raking light helps. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/07_field_linguistics_assistant.ipynb) | Field linguistics assistant | For field linguists: text, symbols and articulation described in one sentence, with IPA where it applies. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/08_psychology_observation_assistant.ipynb) | Psychology observation assistant | For psychologists: an objective description of a room or a task set-up. It does not diagnose, and nobody is observed without informed consent. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/09_bci_neuro_vision_assistant.ipynb) | BCI and neuro-vision assistant | For BCI and neuroscience work: electrode placement, caps and signal plots, checked for plain faults such as line noise or a loose electrode. The course's robots can be driven by a NeuroSky headset. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/10_universal_tutor.ipynb) | One tutor for any domain | Type the domain you are working in, and the same assistant adapts its prompt to it: robot wiring, surgical trays, Brahmi inscriptions or EEG caps. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/11_systems_architecture_sysml.ipynb) | Systems architecture in SysML | Describe a system and get PlantUML for a SysML block definition diagram, compiled and shown in the notebook. The example is a CubeSat. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/12_app_generator.ipynb) | An app from a sentence | Describe a web app; the model writes a single-page app, zips it, and the notebook shows how to publish it from a phone. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/13_cloud_app_generator.ipynb) | A full stack from a sentence | A web front end, a Flask back end and a setup script for a free-tier cloud machine, zipped together. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/14_volunteer_grid_cluster.ipynb) | Notebooks as a volunteer grid | Nginx in front of a small Flask agent, with a shared sheet as the directory, turns many notebooks into a Beowulf-style or BOINC-style grid. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/15_stub_filling_automation.ipynb) | Filling thousands of function stubs | For the operating-systems course: every atomic C function is specified by its interface; a loop fills each stub through an API and zips the tree. The first loop discussed is kept below as well. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/16_backbone_and_mission_control.ipynb) | Backbone and mission control | The environment cell for the Hindawi toolchain, the free signalling backbone on Sheets and Pages, and one tracker for every embodiment, from a toy robot to a CubeSat. |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/ghonchu/blob/main/notebooks/17_coding_agents_and_limits.ipynb) | Coding agents and Colab limits | Coding agents you can run inside Colab, and the session limits to plan around. |

## The course, in brief

Children build the simplest robots that can be made, plastic two-wheel and four-wheel cars, then drones, boats and arms, on Arduino and then ESP32, and code them in their own language through the Hindawi Programming System. The first lesson comes in three timed parts: ten minutes to build, thirty to connect, fifteen to tune. The same notebooks, opened on a phone, carry on to research. The whole concept, and how each notebook fits the course, is in [CONCEPT.md](CONCEPT.md).

## Privacy and safety

Camera pictures go from the phone's browser to a Colab runtime on Google's cloud. Point the camera at the robot, never at a person without their informed consent; children use it with an adult. Nothing here is a medical, psychological or diagnostic device. The notebooks that use the camera say so at the top.

## Licence

GPL-3.0-or-later ([LICENSE](LICENSE)). Cite with [CITATION.cff](CITATION.cff).

<!-- trademarks:begin -->
---
AyeAI® and AyeAM® are registered trade marks of Abhishek Choudhary in India; AyeCNSe™ (Indian TM application No. 7415871, pending) is his trade mark. The names of his products and projects, Ghonchu among them, are his trademarks; see [legal/TRADEMARKS.md](legal/TRADEMARKS.md). Code licences in this repository grant copyright permissions only and no right in any mark.
© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.
<!-- trademarks:end -->
