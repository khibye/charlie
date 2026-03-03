The pseudo code (for python) that I'm looking for is:

The main screen does:
1. Fetches Mongo docs to receive all data relevant that has (country, city) within a date range received.
2. Fetches user_context from contexts mongo table that is unique per (country, city, user_id).
3. Calls ArticleLLMCreator service with all fetched data, user_context, user_id.
4. Shows it in the app.

ArticleLLMCreator pipeline:
input: fetched data, user_context (example: "I am interested in all data that is related to Big Companies"), user_id and a prompt (example: "Write a concise analytical article summarizing the data in relation to the context. Focus on thematic patterns and indirect signals, include insights and conclusions, and avoid mapping individual data points. Do mention important names, places, files and dates. Avoid ignoring and losing important data.").

1. Hold a LLM agent.
# Should be better architected in order to get the best results and finding as much patterns and behaviors as possible: 
1. Async for loop on the fetched data in batches (as big as possible):
	2.1. Sends the batch to the LLM agent with the context and prompt.
2. Get the article after inserting all data to the LLM agent.
3. Return it to the UI.

ContextImprover:
# 2 pipelines:
pipeline 1. Manually change it.
pipeline 2. Gets natural language context and using LLM to build a prompt that writes a context that represents it.


IT SHOULD NOT NECCESSARILY BE DETERMINISTIC!
