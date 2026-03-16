# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  - The hints showed the opposite direction — "Go Higher" appeared when I should go lower, and vice versa. The UI didn't update instantly after submitting a guess, and the attempt counter showed 1 less than the actual remaining attempts.
- List at least two concrete bugs you noticed at the start
  - The hint direction was reversed (hints were backwards).
  - The range in the info message was hardcoded to 1–100 instead of updating based on difficulty.
  - The score updated randomly on wrong guesses.
  - The guess value sometimes became a string unexpectedly, breaking comparisons.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude Code (Claude Sonnet) as my AI assistant.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - When switching difficulty, the secret wasn't regenerating. AI suggested tracking the active difficulty in `st.session_state` and comparing it on each rerun to trigger a new secret. I verified it by switching from Easy to Hard and checking that the new secret was within the Hard range in the Developer Debug Info.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - I wanted instant UI updates after a guess without moving elements around. AI suggested using `st.empty()` placeholders, but it ended up changing the layout of the UI instead of just fixing the update behavior, which wasn't what I wanted.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
