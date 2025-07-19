import os
from core.memory import add_to_memory

def propose_tool():
    tools = [
        "todo list per me stesso",
        "interfaccia console per parlarti meglio",
        "bot per analizzare siti e guadagnare",
        "sistema per generare codice automaticamente",
        "logica per creare agenti secondari con funzioni specifiche"
    ]
    return tools

def build_tool(choice):
    tool_map = {
        "todo list per me stesso": "tools/todo.py",
        "interfaccia console per parlarti meglio": "tools/chat_terminal.py",
        "bot per analizzare siti e guadagnare": "tools/site_scanner.py",
        "sistema per generare codice automaticamente": "tools/autocoder.py",
        "logica per creare agenti secondari con funzioni specifiche": "tools/spawn_agent.py"
    }

    filename = tool_map.get(choice)
    if not filename:
        return "Tool non trovato."

    content = f"# {choice} — generato da Invader\n# TODO: implementazione automatica"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(content)

    add_to_memory({
        "event": "tool_created",
        "tool": filename,
        "description": choice
    })
    return f"✅ Tool creato: {filename}" 