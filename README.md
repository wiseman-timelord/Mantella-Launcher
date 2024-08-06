# Mantella-WT - Drop-in files for Optimization and Enhancement of original scripts. 
Status: Project being re-planned.  Notice: Some of the details are somewhat inaccurate, at-least until the next release.

# Description
So far character descriptions have basic details and 1 sentence description, this helps greatly with faster processing, however, they need to be re-done, to have 2-3 sentences per character. Soon there willbe 2 batches. The batch/python standalone launcher has moved to [Mantella-Local-Launcher](https://github.com/wiseman-timelord/Mantella-Local-Launcher).

# Features
This section is being re-done, however...
- There will be a "Setup-Install.Bat", for requirements, to make things fool-proof.
- There will be a "Run_Mantella.Bat", this will have the epic batch code from the Launcher.
- There will be enhanced versions of main branch scripts, that will be pushed to main or not, 

# Preview
- The working of the thing, is pretty much the same as Mantella, there will be an update here....

## Requirements
1. **Python Environment**: Requires Python 3.11 and dependencies from the Mantella requirements file.
2. **Language Model**: Use [Lewdiculous L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix](https://huggingface.co/Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix) with Q3 or Q4 VRAM specifications.
3. **Operating System**: Compatible with Windows 7 through Windows 11; administrative privileges will be needed.

# Usage / Install
1. Ensure the [Mantella Mod](https://www.nexusmods.com/fallout4/mods/79747) is installed for Fallout/Skyrim from the Nexus mods site, follow the guide, this will, at some point, require install [Mantella 11.4](https://github.com/art-from-the-machine/Mantella/releases/tag/v0.11.4) to a suitable directory.
2. After completing Mantella 11.4 install, then download the [Latest working Mantella-WT release](https://github.com/wiseman-timelord/Mantella-WT/releases/), drop the files into the main Mantella folder, preserving folders.
5. Configure the ".\config.ini", ensure you have entered things like, "fallout4_folder" and "fallout4_mod_folder" and "llm_api" and "tts_service".
6. Run Fallout 4/Skyrim, and then run the `Run_Mantella.Bat` batch.
- Hopefully you have, Admin rights and sensible system settings, but click allow on firewall as required, I am guessing its the interaction between Mantella and the Mantella Mod.

## Notes
- a Llama 3 Q3_m model with fallout 4 dlc & ~300 mods including PhyOp performance texture pack, utilizes all of the 8GB on a single card, if you want to use =>Q4 and/or hd textures, then I suggest 10-12GB free VRam or, sharing processing with the cpu. If you need more VRam, try the "PhyOp" Performance/Regular Textures on Nexus, ensure it loads after things like, for example, CBBE and BodyTalk.

# Development
- Its looking likely, I have determined how to correctly process the character files pre-launce, to the context, and thus, no modified game files are required for deployment, this then becomes the launcher. so the forked files would be gone. it would become a standalone exe, it will be put on, Github repository and nexus, as Mantella-Launcher.
- The idea is now to, 1. optimize the scripts, 2. enhance the prompting, therefore, code in mantella-wt will be able to be pushed to main.
- Streamline the scripts for local should become a diff fork Mantella-Local,  Mantella-Local will then become a thing, for people whom will not be using online services. code will be streamlined, streamlining will open up possibilities. Mantella-Local will not be happening until other projects are complete.
- When v12 comes, We will see what happens. 
1. last thing from the original outline: develop my program to standardize the character csv files, it needs to generate 3 files, 1/2/3 sentence versions, that will be used, relevantly and dynamically, with the context lengths of, 2048, 4096, 8192. What would be simpler is, I could rename the files, ie "gamename_characters.bak", then process it according to the current context settings for context, and over-write any existing csv file in the same dir, so as, to not need a bunch of modifications to, 3 scripts to make them dynamic.
2. Ollama does not have a curl requires, but we know it running or not by "ollama.exe". From command "Ollama Ps", we can find this...
```
NAME                    ID              SIZE    PROCESSOR       UNTIL
qwen2_57b:latest        9dbf41c98d9e    48 GB   100% CPU        4 minutes from now
```
...there is the model name, so we can search the host computer for "qwen2_57b", to find the folder it is in, it will stop on the first one it finds. I would think, that commonly, people would have their models in one location, not duplicated. If we can implement this, then Mantella-Local will be able to support ALL local features. Obviously, it should first check if both Ollama AND LM Studio are running, and if so, then ask the user to choose which one they are using. If multiple models are hosted on ollama/lm studio, then the user should be prompted to choose.
2. Possibly requires advance of my project for utilizing llama.cpp pre-compiled binaries for vulkan, to host models with OhLlama/LmStudio compatibility for apps, as they are not utilizing threads properly or vulkan at all, currently.
3. Noticing the improvements in Language models, 1 token per word? it used to be 5 tokens for every 4 letters, and 4 tokens for every 3 tokens, or something was the calculation, when we were at llama 1 stage, if I am not hallucinating, this is highly impressive advancements, but requires re-assessment of what is a "Required number of Tokens". 
4. Launcher GUI.
5. When they release v12, I am assuming i will have completed/tested this project, so at that point, I will upgrade the main v12 scripts, and push it to main, but whatever code I do push, must, remain compatibly with or expand upon, the Authors intended features, so...I'm guessing that would be the work on the dynamic context size / prompts, try and offload the updates to the mantella team, and focus on the launcher as a separate. as possible, the main scripts should not be touched.


# Disclaimer
- The extension `-WT` means that this project does not originate from Wiseman-Timelord, it is the "Wiseman-Timelord's" own, "Hack" or "Version", of the relating "Official" software. Any issues regarding the "Original" code, stop with the Author's of the "Original" code.
