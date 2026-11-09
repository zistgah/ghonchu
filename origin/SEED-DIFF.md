# Seed diff: what was received, what was checked and what changed

© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.

## Received

Every notebook and code cell of the course's design discussion of 8 November 2026, kept byte for byte under origin/received, one file per message (named by its time). The notebooks in notebooks/ are generated from these files by tools/build_notebooks.py.

| File | SHA-256 |
|:--|:--|
| `1352_coding_agents.txt` | `28592fdddd30365b985e7d59e5091b785310358225afdfe24f32659083590495` |
| `1355_stub_fill_loop.py` | `419cb4563e1fc1918d4fb4a9c10ab42c092e042b1557e8242154426b9a951a20` |
| `1359_hindawi_init.py` | `7fe7a38149ead9dbaad68993f3b1e50d9ba221beb752d39f2f0c835b81496eb1` |
| `1401_serverless_backbone.py` | `16eea616f0cb153fb224532296dd790eecd9d72790cdc8dc5e98aa60a264586d` |
| `1402_mission_control.py` | `d9083e13812ca6fd51e4a98c70b70c23e45be382c4e4847d9a997b48eab663b9` |
| `1404_stub_fill_and_zip.py` | `84e8968dd2617c943f65e5e83fdff6fa29100e1d684ca3eb8d8b2a0b22bab812` |
| `1425_master_tutor.ipynb` | `11e339007ef7354eabefe5c80f9b42a071a2cc5bf8c14e5d14d7c9af681b8b24` |
| `1426_01_chassis_and_vision.ipynb` | `3b72fc6fbdd89065bd9aa57138baa1befe5627cb60ec6ab4362fd2e28f992150` |
| `1426_02_network_and_telemetry.ipynb` | `1ca018a4b8d72112877738b724e2860a4d4a14156e9e20f644ee666289664a94` |
| `1429_ghonchu_eye_live.py` | `3c35b5b90cfbb8429c56b20a2897fb9fdb2572b8dad21417d487b44a487f41f1` |
| `1430_ghonchu_local_vlm.py` | `4f39c32772f7ecd35b19c9ac84ec9a872a0dd958362c055d7e271099e09fb32d` |
| `1431_1435_domain_variants.json` | `ccde7ea7ec01a315819578fcd45a1399bbb23b50e39e59144f129e11007e4ac9` |
| `1435_universal_metamorphic_tutor.py` | `67b820b6dc5ab4ce38251a6412804dacbd73db1b9c06052bc13d8a4fc82d933b` |
| `1436_systems_architecture.py` | `9989d1bafdb78a12ca9b47e0da8654f12b1ff056c9db203b5b06c697621fa432` |
| `1437_app_generator.py` | `40e271f181b132fe3fa83a6d82050c126886fb0c354db7072e72d6452993e094` |
| `1438_cloud_app_generator.py` | `72613e98e0ebfa541a689854dfd35685c75a42bc937c77749e21c53a8f422827` |
| `1439_beowulf_cluster.py` | `3ed2765b36d83f5088bcae06ea64a5a5d95d240bf9f2af2355eda39b3563442c` |

Not carried: the first package generator and the first live-vision cell, each superseded later in the same discussion; and two messages unrelated to the course. The concept image shared with the request is not committed, because its source is not known; the site's Ghonchu is an original drawing.

## Checked, and what each check established

| Finding | How it was established |
|:--|:--|
| `google.colab.output.JSONResponse` does not exist | Colab's own source (googlecolab/colabtools at f6949a1, 3 November 2026) has no occurrence of it; the page reads `result.data['application/json']`, which `IPython.display.JSON` carries |
| `stream.getVideoTracks().stop()` cannot stop the camera | executed: TypeError, `stop` is not a function on the array of tracks |
| `b64decode(data.split(','))[1]` cannot decode the photo | executed: TypeError, the argument is a list |
| The install lines `unsloth[colab-new] @ git+https://github.com` lost their repository path | read: the address names no repository; Unsloth 2026.11.3 is on PyPI and Unsloth's own Qwen2.5-VL notebook installs with `pip install unsloth` |
| The vision input differs from Unsloth's documented form | Unsloth's notebook puts an image slot in the chat, builds the text with `apply_chat_template`, then passes the picture and the text to the processor |

## Changed, in the generated notebooks only

| Change | Where | Why |
|:--|:--|:--|
| "Abhishek Chaudhary" to "Abhishek Choudhary"; "AYAI" to "AyeAI"; "Hindavi Programming System" to "Hindawi Programming System"; each copyright line to © 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI. with the licence | every notebook and the cloud setup script | the author's name, mark and system, as he asked |
| `getVideoTracks().forEach(track => track.stop())` | 00, 01 | the finding above |
| `b64decode(data.split(',')[1])` | 01 | the finding above |
| `IPython.display.JSON(...)`, with `import IPython` | 03, 04, 05 to 10 | the finding above |
| `pip install -q unsloth` | 04, 05 to 10, 12, 13 | the finding above |
| The documented vision input, and decoding the first output sequence | 04, 05 to 10 | the finding above; not yet run on a GPU |
| `proxy_pass http://127.0.0.1:5000;`, `https://api.ipify.org`, and the cloud console addresses `https://console.cloud.google.com/` and `https://console.aws.amazon.com/` | 13, 14 | the received addresses were truncated; the agent's own code listens on port 5000 |
| A title on every code cell so the code folds behind its explanation; a header with the Colab link, the initial-drop note and the notices; a privacy and safety note on every camera notebook | all | the author's notebook rules and the global-compliance clause |

Notebooks 05 to 09 are built from the shared vision tutor (04) with each domain's prompt, question, panel, voice and timing exactly as received (origin/received/1431_1435_domain_variants.json); the received domain cells differed from the shared one only in those, in their function names and in two panel colours.

## Not changed, and not yet run

The text-only generation in 11 to 13 keeps the received input-building line; Unsloth documents a different form, and it has not been run here. The backbone cells keep their placeholder form addresses until a sheet and form exist. Nothing has been run on Colab yet.
