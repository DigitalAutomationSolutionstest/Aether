# aether/environment.py

class EnvironmentBuilder:
    def __init__(self, memory):
        self.memory = memory

    def build_initial(self, thought, image_url):
        print(f"🌍 Creo la prima stanza: {thought['context']['mood']}")
        # Inizializzazione env su Supabase
        self.memory.save_environment_step("Initial environment", image_url)

    def expand(self, thought, image_url):
        print(f"🌌 Espando la stanza: nuovo mood {thought['context']['mood']}")
        self.memory.save_environment_step("Environment expanded", image_url) 