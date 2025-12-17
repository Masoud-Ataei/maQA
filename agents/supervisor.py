class SupervisorAgent:
    def evaluate(self, test_id, actions, errors):
        if errors:
            print(f"[Supervisor] TEST {test_id} → FAIL")
            return "FAIL"

        print(f"[Supervisor] TEST {test_id} → PASS")
        return "PASS"
