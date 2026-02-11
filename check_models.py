import google.generativeai as genai

genai.configure(api_key="AIzaSyD2KfhCwsKDdZOI8fZVNNcZK3dDZHKzPcY")

for m in genai.list_models():
    print(m.name, " → ", m.supported_generation_methods)
