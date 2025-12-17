from tools import adb

class ExecutorAgent:
    
    # # agents/executor.py
    # def execute(action):
    #     if action == "tap_create_vault":
    #         adb.tap(540, 1600)

    #     elif action == "type_vault_name":
    #         adb.type_text("InternVault")
    #         adb.tap(900, 1800)  # confirm
    def screenshot(self):
        path = adb.screenshot()
        return path

    def execute(self, action: str):
        print(f"[Executor] {action}")

        if action == "open_obsidian":
            adb.adb("shell monkey -p md.obsidian 1")

        elif action == "tap_new_note":
            adb.tap(500, 1150)  # example coords

        elif action == "type_title":
            adb.type_text("Meeting Notes")

        elif action == "type_body":
            adb.type_text("Daily Standup")

        elif action == "open_settings":
            adb.tap(100, 200)

        elif action == "find_print_to_pdf":
            # Intentionally fails
            raise RuntimeError("Print to PDF not found")
        
        adb.screenshot()
