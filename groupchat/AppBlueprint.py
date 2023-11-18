# filename: AppBlueprint.py

class App:
    def __init__(self, name="Pocket Concierge"):
        self.name = name
        self.platforms = ["platform_1", "platform_2"]
        self.features = ["feature_1", "feature_2", "feature_3"]
        self.user_interface = ["UI_component_1", "UI_component_2", "UI_component_3"]

    def describe(self):
        print(f"App Name: {self.name}")
        print("Platforms: ")
        for platform in self.platforms:
            print(f"\t- {platform}")
        print("Features: ")
        for feature in self.features:
            print(f"\t- {feature}")
        print("User Interface components: ")
        for ui in self.user_interface:
            print(f"\t- {ui}")

app_blueprint = App()
app_blueprint.describe()