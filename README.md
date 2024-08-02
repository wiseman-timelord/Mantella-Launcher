# Mantella-WT - Wiseman-Timelords Mantella Fork
This is a fork, [main is here](https://github.com/art-from-the-machine/Mantella)

# Completed
1. Batch launcher, that launches BOTH, xVASynth in non-Admin AND Mantella in Admin, for minimal hastle...
- This requires install xVASynth to `.\ExampleMantellaDirectory\xVASynth`, but I dont think 99% of people will use xVASynth with other things, so it should probs go in mantella dir somewhere, then its still good for, skyrim or fallout, etc. I dont run Mantella without it. BEsides other things, mantella can mess up and need a restart, and I might forget to close xVASynth. I also dont want to have to go to 3 total locations to run essentially one program. The batch saves time and messing around. 


# Development 
- Dynamic switching between prompt sets for differing context, depending upon the maximum context for the model, we could work up to that, possibly we could switch between 2000, 4000, 8000, however, we would also not just use the maximum all the time. Its my opinion that a ok and fast, answer from AI is better than waiting for a quality response, especially in fps, and in relevance to Fallout 4/Skyrim, these are meant to be 100% offline, so I am leaning towards local models heavily..
1. Potentially requiring 3 versions of the characters .csv and prompts.
2. we would use the better quality one after 2 of shorter one so as, for the time taken to increase gradually, as well as, the quality of the output, thereabouts the user sets the maximum context it will dynamically use. A flag will be reset when convo ends..
3. Smaller but dynamic, consolidated information at end of convo. The main delay is feeding in the Initial prompt for each character, at the start of the convo, again, this is optimized for 8192 context, this is likely being lopped off on 4k, either way its too much for local models at 8k.
4. Some of the inputs, can actually be dynamic, and not present at all in user interaction, most/some of this could scale based on context size and be reasonable settings, For examples...

# Description
- The edits to actual mantella code will be for v11, until they get v12 relesaed. There is something wrong with the communication between the, fallout 4 mod and mantella, in v12.

# v12 Notes
- Mantella v11 saves the config.ini in a safe location of the mantella dir, however, with regards to v12, I moved my documents folder from `C:\users\username\my documents\` to a different drive, and for some reason Mantella v12 insists upon using the vanilla windows docs dir on C: for `config.ini`, otherwise, my launcher could have looked in the config.ini to find where xVASynth is. So likely it will move again in v12.1 or whatever when they correct it. Personally I would not  leave local folders, and just, for example `.\ExampleMantellaDir\Data\config.ini`, if I wanted to hide it. There is no reason to preserve settings between versions as far as v11 to v12 is concerned, and with regards to what I higlight below, there is no need for so much configuration, so the config file will change.

# Other Notes
- Dynamic Context
```
2048
max_tokens = 100
max_response_sentences = 1
temperature = 0.4

4096
max_tokens = 125
max_response_sentences = 2
temperature = 0.5

8192
max_tokens = 150
max_response_sentences = 2
temperature = 0.6
```
... the maximum allowed context would also work together with the auto model selection, because the user would be able to therein set the maximum they intend to use. Maybe they just want to use 2k on a 8k model for speed, but if they want to wait for local processing or they are using gpt4, then they would choose to set higher.
- This is the more concise code for the ini from Nexus.
```
skyrim_multi_npc_prompt = Not needed.

fallout4_prompt = You are {name} in the post-apocalyptic Commonwealth of Fallout. This is your background: {bio}. In-game events will be shown between ** symbols for context. You're having a conversation with {trust} (the player) in {location}. The time is {time} {time_group}. This script will be spoken aloud, so keep responses concise. Avoid, numbered lists or text-only formatting or descriptions, instead speech ONLY. If the player is offensive, start with 'Offended:'. If they apologize or to end combat, start with 'Forgiven:'. If convinced to follow, start with 'Follow:'. The The conversation is in {language}. {conversation_summary}

fallout4_multi_npc_prompt = The following conversation in {location} in the post-apocalyptic Commonwealth of Fallout is between {names_w_player}. Their backgrounds: {bios}. Their conversation histories: {conversation_summaries}. The time is {time} {time_group}. This script will be spoken aloud, so keep responses concise. Avoid, numbered lists or text-only formatting or descriptions, instead speech ONLY. Provide NPC responses, starting with the speaker's name, e.g., '{name}: Good evening.' Decide who should speak as needed (sometimes all NPCs). Respond only as {names}. Use full names. The conversation is in {language}.

radiant_start_prompt = Start or continue a conversation topic (skip greetings). Shift topics if current ones lose steam. Steer toward character revelations or drive previous conversations forward.

radiant_end_prompt = Wrap up the current topic naturally. No need for formal goodbyes as no one is leaving.

memory_prompt = Summarize the conversation between {name} (assistant) and the player (user)/others in {game}. Ignore communication mix-ups like mishearings. Summarize in {language}, capturing the essence of in-game events.

resummarize_prompt = Summarize the conversation history between {name} (assistant) and the player (user)/others in {game}. Each paragraph is a separate conversation. Condense into a single paragraph in {language}.
```
- Some new code to enhance local model ease of use.
```
Drop in your preferred Llama.Cpp Pre-Compiled binaries? All I can think of for now. 
```
- sensible base settings...
```
pause_threshold = 1.5 
```

# Description
- These edits will be, paused or for v11, until they get v12 figured out, something wrong with the communication between the, fallout 4 mod and the main, possibly they are using some development version of the Fallout 4 mod I am not, or the fallout 4 side needs updating.

# Preview
- Uh, theres the batch launcher...
```
==============================================================================
                         Mantella / xVASynth Launcher
------------------------------------------------------------------------------

Admin Mode: Correct
Current Directory: D:\GamesVR\Mantella-0.12_preview
Checking for running xVASynth.exe process...
xVASynth.exe is already running. Closing it now...
xVASynth.exe has been closed.
Running VASynth and Mantella...
Mantella.exe running in:
D:\GamesVR\Mantella-0.12_preview
config.ini, logging.log, and conversation histories available in:
C:\Users\Mastar\Documents\My Games\Mantella\
Mantella currently running for Fallout4. Mantella mod files located in:
D:\GamesVR\Fallout4_163\Data\Sound\Voice\Mantella.esp

Mantella v0.12 Preview
20:50:40.793 INFO: HTTP Request: GET https://api.gradio.app/gradio-messaging/en "HTTP/1.1 200 OK"
Running Mantella with 'Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix'. The language model can be changed in MantellaSoftware/config.ini
20:50:44.182 TTS: Connecting to xVASynth...
20:50:44.498 INFO: Mantella settings can be changed via this link: http://localhost:4999/ui?__theme=dark

Conversations not starting when you select an NPC? See here:
https://art-from-the-machine.github.io/Mantella/pages/issues_qna

Waiting for player to select an NPC...

```

# Disclaimer
- This is a fork by Wiseman-Timelord, meaning, if you have issues with the program, its Likely not my code, you would have to check that.
- My forks sometimes just up and dissapear, this tends to happen when I no longer use the relating program, to neaten up things a little.
