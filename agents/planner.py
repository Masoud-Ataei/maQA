class PlannerAgent:
    def plan(self, test_text: str):
        """
        Output a list of high-level actions.
        """
        if "create a new Vault" in test_text:
            return [
                "open_obsidian",
                "click_create_vault",
                "type_vault_name",
                "confirm"
            ]

        if "Create a new note" in test_text:
            return [
                "tap_new_note",
                "type_title",
                "type_body"
            ]

        if "Appearance tab icon is the color Red" in test_text:
            return [
                "open_settings",
                "check_appearance_icon_color"
            ]

        if "Print to PDF" in test_text:
            return [
                "open_file_menu",
                "find_print_to_pdf"
            ]

        return []
    
    class PlannerAgent:
        def next_action(self, goal, vision_state):
            screen = vision_state["screen"]
            elements = vision_state["elements"]

            if goal == "create_vault":
                if screen == "welcome_screen":
                    return "tap_create_vault"

                if screen == "vault_creation":
                    return "type_vault_name"

                if screen == "inside_vault":
                    return "done"

            return "fail"
