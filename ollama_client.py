import requests, json

def call_ollama(prompt: str, model: str = "llama3.2:1b", base_url: str = "http://localhost:11434"):
    url = f"{base_url}/api/generate"
    resp = requests.post(url, json={"model": model, "prompt": prompt}, stream=True)
    if not resp.ok:
        raise RuntimeError(resp.text)

    output = ""
    for line in resp.iter_lines():
        if line:
            j = json.loads(line.decode("utf-8"))
            if "response" in j:
                output += j["response"]
            if j.get("done"):
                break
    return output.strip()