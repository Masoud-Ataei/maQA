from PIL import Image
import base64
import json
from google import genai 
from google.genai import types
import os

# def encode_image(path):
#     with open(path, "rb") as f:
#         return base64.b64encode(f.read()).decode()

class VisionAgent:
    def __init__(self):
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        self.client = genai.Client()

    def image_to_text(self, image_path, prompt_text = ""):
        """
        Generates text from an image using the Gemini model.

        Args:
            image_path (str): The local path to the image file.
            prompt_text (str): The text prompt to guide the model.

        Returns:
            str: The generated text from the model.
        """
        img = Image.open(image_path)

        prompt = f"""
                    You are a mo```bile QA assistant.

                    Look at the screenshot and answer ONLY with a JSON object.
                    The image is the screenshot of a cellphone, and it is Obsidian program.

                    Classify the current Obsidian screen as one of:
                    - "welcome_screen"
                    - "vault_creation"
                    - "inside_vault"
                    - "settings"
                    - "unknown"

                    Also list visible UI elements only Buttons and Labels.

                    Respond in JSON:
                    {{
                    "Screen": "...",
                    "Elements": ["...","..."]
                    }}
                    """
        # Create the multimodal content list
        # The model processes both the image and the text prompt
        content = [prompt + prompt_text, img]

        # Call Gemini / GPT-4V / etc.
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=content,
        )
        return json.loads(response)
    
    # def call_llm_with_image(promp, image)
