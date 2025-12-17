Decision Memo: Framework Selection for Mobile QA Agent
After evaluating the architectural requirements for a Mobile QA Agent, I selected Google Agent Development Kit (ADK) as the agent orchestration framework. ADK provides a clean abstraction for defining agent roles, model configuration, and tool usage, making it well-suited for structuring a multi-agent system with clear responsibility boundaries.
ADK’s Agent–Runner execution model enables controlled interaction between language models and external tools, which aligns well with mobile QA automation where reasoning, execution, and verification must remain explicitly separated. The ADK supports session-based execution system uses a stateless agent execution pattern, with test state tracked externally by the supervisor logic for improved determinism and debuggability.
Architecture Design
The system is designed as a Supervisor–Planner–Executor multi-agent architecture with an auxiliary Vision and Evaluation component.
Agent Responsibilities
Supervisor Agent
Receives natural language QA test cases and orchestrates the overall execution flow. It manages test state, requests screenshots, routes information between agents, and determines when the test has completed or failed.
Planner Agent
Interprets natural language QA test cases and decomposes them into a sequence of executable, atomic UI actions. The planner reasons over the current application state (derived from screenshots or execution history) but does not interact with the device directly.
Executor Agent
Executes structured UI actions using deterministic ADB-based tools such as tap, swipe, text input, screenshot capture, and app launch. The executor does not interpret natural language or perform planning.
Vision Agent
Analyzes screenshots provided by the Supervisor to infer the current UI state of the Obsidian app (e.g., welcome screen, vault creation screen, inside vault). This information is returned in a structured format and used to guide planning and verification.
Evaluator Agent
Verifies whether the executed actions satisfy the test assertions and reports a final PASS / FAIL outcome. It distinguishes between execution failures (e.g., UI element not found) and assertion failures (e.g., expected feature does not exist).
Execution Flow
The Supervisor Agent receives a natural language QA test case.
The Planner Agent converts the test into executable UI actions.
The Executor Agent performs each action on the Android emulator.
Screenshots are captured and analyzed by the Vision Agent to infer app state.
The Evaluator Agent validates outcomes and reports test results.
The Supervisor logs the final result and proceeds to the next test.
Rationale
This architecture cleanly separates reasoning, execution, and verification concerns, enabling deterministic mobile QA automation while preserving agentic behavior. Google ADK provides a flexible foundation for defining agent roles and integrating language models without coupling high-level reasoning directly to low-level device control.


