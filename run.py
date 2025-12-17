from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.supervisor import SupervisorAgent
from tests.qa_tests import QA_TESTS
from tools.vision import VisionAgent
from dotenv import load_dotenv

load_dotenv()

planner = PlannerAgent()
executor = ExecutorAgent()
supervisor = SupervisorAgent()
vision   = VisionAgent()
for test in QA_TESTS:
    print(f"\n=== Running Test {test['id']} ===")
    plan = planner.plan(test["text"])

    errors = []
    # for step in plan:
    #     try:
    #         executor.execute(step)
    #     except Exception as e:
    #         print(f"[Error] {e}")
    #         errors.append(str(e))
    #         break

    goal = "create_vault"

    while True:
        screenshot_path = executor.screenshot()
        vision_state = vision.analyze(screenshot_path)

        action = planner.next_action(goal, vision_state)

        if action == "done":
            print("✅ Goal achieved")
            break

        if action == "fail":
            print("❌ Cannot proceed")
            break

        executor.execute(action)

    result = supervisor.evaluate(test["id"], plan, errors)
    print(f"Expected: {test['expected']} | Got: {result}")
