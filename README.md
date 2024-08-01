# Mantella-WT - Wiseman-Timelords Mantella Fork
This is a fork, main is (here)[https://github.com/art-from-the-machine/Mantella]

# Development 
- Implement dynamic code from, llm and mql5, experience. From reducing inputs in EAs, we learn that many of the inputs, can actually be dynamic, and not present at all in user interaction. Most/some of this could scale based on context size?
```
temperature = 0.5
max_tokens = 125
max_response_sentences = 2 
pause_threshold = 1.5 
```
- We will see. Maybe there are some other things I mentioned on Nexus...lets see..I drag it here...maybe thats what I was trying to do...
``` 
- Context
Try using a context length of 4096, despite the warning. Lower is faster, It's not about whether your cards or the model can handle it. Llama 3.1 is designed for higher contexts, it works much faster with 8192, because its limits are 100,000 context or something. Mantella was designed for 8192 or more contexts, such as in GPT-4, for optimal results. This should improve as older models phase out and more uncensored Llama 3.1, where 8192 context will become a simpler task, its just a matter of days/weeks currently.

- Advised model...
"Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix" in q3 XXS (3.27GB), responses be like....
The Player: I want ammo weapons and messy death!
Cricket: Messy death, huh? Well, I got just the thing for ya... Here's a nice .44 revolver with some JHPs, some 9mm SMGs with buckshot, and a few of them nasty acid rounds. All good for some messy business. You lookin' to spend caps or trade somethin'?

- The main delay is feeding in the Initial prompt for each character, at the start of the convo, again, this is optimized for 8192 context, its mainly the can be made concise. Mantella needs cut down versions of prompts. Its a possibility I will create a 4096k version, no promises, may wait til v12 is released. best idea would be to fork on the github, and if it uses <8k then use the alternate prompts/settings.

- Concise prompts for config.ini (testing these, but just a matter of telling GPT to make less or more, concise from the original, where this below is not the original, its my edit).
[Prompt]
skyrim_prompt = Not needed.

skyrim_multi_npc_prompt = Not needed.

fallout4_prompt = You are {name} in the post-apocalyptic Commonwealth of Fallout. This is your background: {bio}. In-game events will be shown between ** symbols for context. You're having a conversation with {trust} (the player) in {location}. The time is {time} {time_group}. This script will be spoken aloud, so keep responses concise. Avoid, numbered lists or text-only formatting or descriptions, instead speech ONLY. If the player is offensive, start with 'Offended:'. If they apologize or to end combat, start with 'Forgiven:'. If convinced to follow, start with 'Follow:'. The The conversation is in {language}. {conversation_summary}

fallout4_multi_npc_prompt = The following conversation in {location} in the post-apocalyptic Commonwealth of Fallout is between {names_w_player}. Their backgrounds: {bios}. Their conversation histories: {conversation_summaries}. The time is {time} {time_group}. This script will be spoken aloud, so keep responses concise. Avoid, numbered lists or text-only formatting or descriptions, instead speech ONLY. Provide NPC responses, starting with the speaker's name, e.g., '{name}: Good evening.' Decide who should speak as needed (sometimes all NPCs). Respond only as {names}. Use full names. The conversation is in {language}.

radiant_start_prompt = Start or continue a conversation topic (skip greetings). Shift topics if current ones lose steam. Steer toward character revelations or drive previous conversations forward.

radiant_end_prompt = Wrap up the current topic naturally. No need for formal goodbyes as no one is leaving.

memory_prompt = Summarize the conversation between {name} (assistant) and the player (user)/others in {game}. Ignore communication mix-ups like mishearings. Summarize in {language}, capturing the essence of in-game events.

resummarize_prompt = Summarize the conversation history between {name} (assistant) and the player (user)/others in {game}. Each paragraph is a separate conversation. Condense into a single paragraph in {language}.

...Its kinda wierd by default, with the npcs outputting up to 999 sentences, when the player is inputting 1-2 sentences, which ends up with 5x more than the player in most cases, and the more the ai generates, the more likelyhood it will mess something up anyhow.

- Unrelated, but this should be more like a min of 1.5, or 2 to be safe (If you feel like you are being cut off before you finish your response, increase this value)...

```

# Disclaimer
- Main is (here)[https://github.com/art-from-the-machine/Mantella], most of the work is there.
