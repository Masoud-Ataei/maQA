import subprocess
import time
from google.adk.agents import Agent
import os

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

import asyncio
from google.genai import types
import nest_asyncio
nest_asyncio.apply()

ADB = "~\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"

def tap(x, y):
    """
    Perform a single tap gesture on the device touchscreen.

    This tool simulates a human finger tap at a specific screen coordinate.
    It is typically used to press buttons, select UI elements, or focus input fields.

    When to use:
    - Clicking buttons (e.g., "Create Vault", "New Note")
    - Selecting menu items
    - Focusing a text input field

    Parameters:
    - x (int): Horizontal pixel coordinate from the left of the screen.
    - y (int): Vertical pixel coordinate from the top of the screen.

    Notes:
    - Screen coordinates depend on device resolution.
    - Use `get_coordinates()` to determine valid ranges.
    """
    subprocess.run([ADB, "shell", "input", "tap", str(x), str(y)])

def type_text(text):
    """
    Send text input to the currently focused text field on the device.

    This tool simulates typing text using the Android input system.
    It assumes that a text field is already focused.

    When to use:
    - Entering vault names
    - Writing note titles or note body content
    - Filling text fields in dialogs or forms

    Parameters:
    - text (str): The text to type into the focused input field.

    Notes:
    - Spaces are automatically converted to '%s' to comply with ADB input rules.
    - Does not automatically press Enter or confirm submission.
    """
    text = text.replace(" ", "%s")
    subprocess.run([ADB, "shell", "input", "text", text])

def swipe(x1, y1, x2, y2, duration=500):
    """
    Perform a swipe (drag) gesture on the device touchscreen.

    This tool simulates a finger dragging from a start point to an end point.
    It can be used for scrolling, opening drawers, or performing gesture navigation.

    When to use:
    - Scrolling lists or pages
    - Opening side menus
    - Navigating long screens

    Parameters:
    - x1 (int): Starting horizontal pixel coordinate.
    - y1 (int): Starting vertical pixel coordinate.
    - x2 (int): Ending horizontal pixel coordinate.
    - y2 (int): Ending vertical pixel coordinate.
    - duration (int): Duration of the swipe in milliseconds (default: 500).

    Notes:
    - Longer duration results in a slower swipe.
    - Direction of swipe determines scroll direction.
    """
    subprocess.run(["adb", "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])
    # time.sleep(1)

def screenshot(path="screen.png"):
    """
    Capture a screenshot of the current device screen.

    This tool captures the full device display and saves it as a PNG file.
    Screenshots are used by the agent for visual verification, debugging,
    and state assessment.

    When to use:
    - After performing an️action, to verify UI state
    - Before planning the next step
    - For logging and demo recording

    Parameters:
    - path (str): File path where the screenshot will be saved (default: 'screen.png').

    Notes:
    - Overwrites the file if it already exists.
    """
    with open(path, "wb") as f:
        subprocess.run([ADB, "exec-out", "screencap", "-p"], stdout=f)

def open_app(package_name="md.obsidian"):
    """
    Launch an Android application by its package name.

    This tool starts the specified app using the Android launcher intent.
    It simulates a user opening the app from the home screen.

    When to use:
    - Starting the Obsidian app
    - Relaunching the app after a crash
    - Ensuring the app is in the foreground

    Parameters:
    - package_name (str): Android package name of the app to launch
      (default: 'md.obsidian').

    Notes:
    - Does not verify whether the app successfully launched.
    - A short delay after launching is often recommended.
    """
    subprocess.run([
        ADB,
        "shell",
        "monkey",
        "-p",
        package_name,
        "-c",
        "android.intent.category.LAUNCHER",
        "1"
    ])
    # time.sleep(2)

def get_coordinates():    
    """
    Retrieve the device screen resolution in pixels.

    This tool queries the Android window manager to determine the
    physical or overridden screen size. It is useful for calculating
    valid tap and swipe coordinates.

    When to use:
    - Before computing screen-relative tap positions
    - To adapt gestures to different device resolutions

    Returns:
    - (width, height) (tuple[int, int]): Screen resolution in pixels.

    Notes:
    - If an override size is set, it will be returned.
    - Otherwise, the physical screen size is used.
    """
    res = subprocess.run([ADB, "shell", "wm", "size"],  check=True, capture_output=True, text=True)    
    for line in res.stdout.splitlines():
        if line.startswith("Override size"):
            return tuple(map(int, line.split(":")[1].strip().split("x")))
        if line.startswith("Physical size"):
            physical = tuple(map(int, line.split(":")[1].strip().split("x")))
    return physical

class root_agent:
    def __init__(self):
        model_name = os.getenv("MODEL_AGENT")
        if not model_name:
            model_name = "gemini-2.0-flash"
            
        root_agent = Agent(
        name="Planner_Agent",
        model=model_name,
        description=(
            """Planner_Agent is responsible for interpreting natural language QA test cases and converting them into a sequence of executable, 
            atomic UI actions (low-level ADB-based tools such as tap, swipe, text input, screenshots, and open_app). 
            It reasons about the current application state (texts generated from a image to text convertor) and determines 
            the next appropriate action required to progress toward the test goal. 
            The Planner_Agent does not interact with the device directly; instead, it outputs structured action commands 
            that are executed by the Executor.
            The response of Planner_Agent is a list of actions with appropriate parameters.
            """
        ),
        instruction=(
            "You are a helpful agent who can answer user questions about the time and weather in a city."
        ),
        tools=[tap, swipe, type_text, screenshot, open_app, get_coordinates],
        )

        # Create a session (conversation state)
        session_service = InMemorySessionService()

        # Create a runner
        self.runner = Runner(
            agent=root_agent,
            app_name="mobile-qa-helper",  # Add this line
            session_service=session_service  # Pass the service or the session depending on your ADK version
        )
        # session = session_service.create_session(app_name="my_app", user_id="user_123")
        self.session = await session_service.create_session(app_name="mobile-qa-helper", user_id="user_123")
        print(f"Session created with ID: {self.session.id}")
    
    

    async def chat_with_agent(self, user_query = "Hello! What can you help me with today?"):
        # 1. Prepare your message    
        # session = await session_service.create_session(app_name="my_app", user_id="user_123")
        new_message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_query)]
        )

        print(f"User: {user_query}")

        # 2. Execute the runner
        # Note: Use session.id and the same user_id from your session creation
        events = self.runner.run_async(
            user_id="user_123",
            session_id=self.session.id,
            new_message=new_message
        )

        # 3. Process the stream of events
        async for event in events:
            # Check if the event contains the final text response
            if event.is_final_response():
                # Extract the text from the response parts
                response_text = event.content.parts[0].text
                print(f"Agent: {response_text}")
    
        await chat_with_agent(runner, session)