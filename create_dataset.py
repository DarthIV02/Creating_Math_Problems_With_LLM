import sys
import os
import json
import re
from openai import OpenAI
from google import genai
from prompt_creation.prompt_version_2 import build_prompt
import tiktoken

# ------------------------
# Query Helpers
# ------------------------
def parse_JSON(text):
    match = re.search(r"\{.*?\}", text, re.DOTALL)
    if not match:
        print("⚠️ No JSON found in response:")
        print(text)
        return None

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        print("⚠️ Invalid JSON returned:")
        print(text)
        return None

def query_openai_json(client_openai, model_name, prompt):
    """
    Sends prompt to OpenAI and extracts first JSON object.
    """
    response = client_openai.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        timeout=60.0
    )

    text = response.choices[0].message.content
    return parse_JSON(text)

def query_gemini_json(client_gemini, model_name, prompt):
    """
    Sends prompt to Gemini and extracts first JSON object.
    """
    response = client_gemini.models.generate_content(model=model_name, contents=prompt)
    text = response.text
    return parse_JSON(text)

# ------------------------
# JSON File Helper
# ------------------------
def ensure_file(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)

if __name__ == "__main__":

    # Process arguments
    if len(sys.argv) != 4:
        print("Usage: python create_dataset.py <model> <grade> <num_problems>")
        sys.exit(1)

    model_name = sys.argv[1]
    grade = int(sys.argv[2])
    num_problems = int(sys.argv[3])

    # Add your API keys
    client_openai = OpenAI(api_key="",
                           timeout=20.0)

    client_gemini = genai.Client(api_key="")

    # Change if you only want a subset of difficulties
    difficulties = ["Einfach", "Mittel", "Schwer"]

    # Change output path of the problems
    os.makedirs("problems", exist_ok=True)
    json_path = f"problems/version_2/{model_name}.json"
    ensure_file(json_path)

    # Always read existing file
    with open(json_path, "r") as f:
        all_entries = json.load(f)

    for difficulty in difficulties:
        print(f"\n🔹 Generating {num_problems} problems for Grade {grade}, Difficulty {difficulty}...")

        for i in range(num_problems):
            prompt = build_prompt(grade, difficulty)

            # Call the API of the LLM
            if model_name == "gpt-4o-mini" or model_name == "gpt-4o-mini":
                query_func = query_openai_json
                client = client_openai
            elif model_name == "gemini-2.5-flash" or model_name == "gemini-2.5-flash-lite" or model_name == "gemini-2.5-pro":
                query_func = query_gemini_json
                client = client_gemini
            else:
                raise Exception("Unknown model: " + model_name)
            
            # Uncomment if you want to return the number of tokens
            # encoding = tiktoken.encoding_for_model(model_name)
            # tokens = encoding.encode(prompt)
            # print("Number of tokens:", len(tokens))
            
            result = query_func(client, model_name, prompt)
            
            # If valid response (p.e. correct JSON response) then save
            if result is not None:
                all_entries.append(result)

                # Immediately save JSON after every problem (crash-proof)
                with open(json_path, "w") as f:
                    json.dump(all_entries, f, indent=2)

                print(f"✔ Problem saved ({len(all_entries)} total)")
            else:
                print("❌ Problem generation failed, skipping.")

    print(f"\n✅ All problems written continuously to {json_path}")
