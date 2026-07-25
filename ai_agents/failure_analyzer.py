import json
import os
import ollama

ANALYZER_MODEL = os.getenv("ANALYZER_MODEL", "qwen2.5-coder:7b")

def failure_analyzer_agent(llm_prompt: str, model_name: str = None) -> dict:
    """
    Sends the Pytest failure context to a local open-source LLM.
    
    Args:
        llm_prompt (str): The formatted context containing the stack trace and artifacts.
        model_name (str): The open-source model to use (e.g., 'qwen2.5-coder:7b', 'mistral', 'phi3').
                         Defaults to ANALYZER_MODEL env var or 'qwen2.5-coder:7b'.
        
    Returns:
        dict: A dictionary containing the root_cause, category, and suggested_fix.
    """
    if model_name is None:
        model_name = ANALYZER_MODEL
    
    # Reinforce the JSON schema constraint. Open-source models can sometimes 
    # ignore instructions and add conversational filler like "Here is your JSON:"
    system_instruction = (
        "You are an expert SDET Failure Analyzer Agent. "
        "You must respond ONLY with valid JSON matching this schema: "
        '{"root_cause": "string", "category": "string", "suggested_fix": "string"}. '
        "Do not include any conversational text or markdown code blocks."
    )
    
    try:
        # Call the local Ollama instance
        response = ollama.chat(
            model=model_name,
            messages=[
                {'role': 'system', 'content': system_instruction},
                {'role': 'user', 'content': llm_prompt}
            ],
            format='json', # Forces the model to output valid JSON
            options={
                'temperature': 0.1, # Keep it low for deterministic, analytical outputs
                'num_predict': 300  # Cap the output length to keep it concise
            }
        )
        
        # Extract the raw text from the LLM's response
        result_text = response['message']['content']
        
        # Parse it into a Python dictionary to send back to the Pytest hook
        analysis_data = json.loads(result_text)
        return analysis_data
        
    except json.JSONDecodeError:
        # Fallback if the LLM hallucinated outside the JSON structure
        return {
            "root_cause": "LLM failed to format response as valid JSON.",
            "category": "Agent_Error",
            "suggested_fix": "Review the raw agent output logs or tweak the system prompt."
        }
    except Exception as e:
        # Fallback if the Ollama service isn't running or the model isn't downloaded
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            suggestion = f"Ensure Ollama is running and model '{model_name}' is pulled. Run: ollama pull {model_name}"
        else:
            suggestion = f"Ensure Ollama is running locally and `{model_name}` is pulled. Check Ollama logs for details."
        return {
            "root_cause": f"Connection to Open-Source LLM failed: {error_msg}",
            "category": "Infrastructure_Error",
            "suggested_fix": suggestion
        }

# --- Quick Local Testing ---
if __name__ == "__main__":
    sample_prompt = """
    Test Name: test_login_flow
    Error Trace: Element <button id="submit"> not interactable after 10000ms.
    UI Context: DOM Snippet shows <button id="submit" disabled="true">
    """
    
    print("Thinking...\n")
    result = failure_analyzer_agent(sample_prompt)
    print(json.dumps(result, indent=2))