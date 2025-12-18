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

    def image_to_text(self, image_path):
        """
        Generates text from an image using the Gemini model.

        Args:
            image_path (str): The local path to the image file.
            prompt_text (str): The text prompt to guide the model.

        Returns:
            str: The generated text from the model.
        """
        img = Image.open(image_path)

        prompt = """
                You are a mobile QA vision specialist. Analyze the provided screenshot of the Obsidian app.
                Classify the screen into one of these specific states:
                - home_screen: Has GMail, Youtube, Photos, and Chrome icons.
                - welcome_screen: Has the button create a vault, the title is your thouths are yours.
                - sync_screen: Has the button 'Continue without sync'.
                - vault_creation: The 'configure your new vault' form/dialog. 
                - folder_selection: 'use this folder'. 
                - inside_vault: Viewing a note or the file explorer.
                - settings: The app settings menu.
                - unknown: Any screen that doesn't fit the above.
                
                Also list clickable Buttons and InputTexts with their x,y BoundingBox.
                Respond in JSON:
                            {
                            "Screen": "...",
                            "Elements": ["...","..."]
                            }
                """
        # Create the multimodal content list
        # The model processes both the image and the text prompt
        content = [prompt, img]

        # Call Gemini / GPT-4V / etc.
        response = self.client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=content,
        )
        return response
    def image_to_text_user(self, image_path, prompt_text = ""):
        """
        Generates text from an image using the Gemini model.

        Args:
            image_path (str): The local path to the image file.
            prompt_text (str): The text prompt to guide the model.

        Returns:
            str: The generated text from the model.
        """
        img = Image.open(image_path)

        # Create the multimodal content list
        # The model processes both the image and the text prompt
        content = [prompt_text, img]

        # Call Gemini / GPT-4V / etc.
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=content,
        )
        return response
    
    def get_screen_state(self, image_path):
        """
        Classifies the mobile screen state into predefined categories.
        """
        # Load the image
        img = Image.open(image_path)
        
        # define the system prompt as a clear set of rules
        system_instruction = """
        You are a mobile QA vision specialist. Analyze the provided screenshot of the Obsidian app.
        Classify the screen into one of these specific states:
        - home_screen: Has GMail, Youtube, Photos, and Chrome icons.
        - welcome_screen: Has the button create a vault, the title is your thouths are yours.
        - vault_creation: The 'Create new vault' form/dialog.
        - inside_vault: Viewing a note or the file explorer.
        - settings: The app settings menu.
        - unknown: Any screen that doesn't fit the above.
        """

        # Use Structured Outputs (Response Schema) to guarantee JSON format
        response_schema = {
            "type": "OBJECT",
            "properties": {
                "screen": {"type": "STRING"},
                "elements": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"}
                },
                "confidence": {"type": "NUMBER"}
            },
            "required": ["screen", "elements"]
        }

        # Generate content using the Lite model for speed/cost
        response = self.client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=[system_instruction, img],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        
        # Parse the guaranteed JSON
        return json.loads(response.text)
    # def call_llm_with_image(promp, image)
