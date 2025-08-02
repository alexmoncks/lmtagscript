
import re
import json

with open("input.tag", "r") as file:
    script = file.read()

# Patterns reused
task_p = re.compile(r"TASK:\s*(.+)")
action_p = re.compile(r"ACTION:\s*(.+)")
goal_p = re.compile(r"GOAL:\s*(.+)")
api_call_p = re.compile(r"CALL API ([\w_]+)\.([\w_]+) WITH \{([^}]+)\}", re.DOTALL)
class_p = re.compile(r"CLASS\s+(\w+)\s+((?:\s+\w+:\s+\w+\s*)+)", re.MULTILINE)
func_def_p = re.compile(r"DEFINE FUNCTION\s+(\w+)\((.*?)\)\s+(TASK:.+?GOAL:.+?)(?=(\nDEFINE FUNCTION|\nCALL|\Z))", re.DOTALL)
func_call_p = re.compile(r"CALL\s+(\w+)\((.*?)\)", re.MULTILINE)
if_p = re.compile(r"IF\s+(\w+)\s*([=!<>]+)\s*(\w+)\s*THEN\s+(.*?)\s*(?:ELSE\s+(.*?))?(?=(\n[A-Z]+:|\Z))", re.DOTALL)
for_p = re.compile(r"FOR EACH (\w+) IN (\w+)\s+(TASK:.+?GOAL:.+?)(?=(\n[A-Z]+:|\Z))", re.DOTALL)
on_error_p = re.compile(r"ON ERROR\s+(TASK:.+?GOAL:.+?)(?=(\n[A-Z]+:|\Z))", re.DOTALL)
loopguard_p = re.compile(r"LOOPGUARD\s*\{\s*max_depth:\s*(\d+),\s*allow_repeat:\s*(true|false)\s*\}", re.DOTALL)

def parse_tags(script):
    res = {}

    def extract(k, p):
        m = p.search(script)
        return m.group(1).strip() if m else None

    res["task"] = extract("task", task_p)
    res["action"] = extract("action", action_p)
    res["goal"] = extract("goal", goal_p)

    m = api_call_p.search(script)
    if m:
        payload = {k.strip(): v.strip().strip('",') for k, v in
                   [line.split(":") for line in m.group(3).strip().split("\n") if ":" in line]}
        res["api_call"] = {
            "service": m.group(1),
            "endpoint": m.group(2),
            "payload": payload
        }

    res["classes"] = {}
    for m in class_p.finditer(script):
        res["classes"][m.group(1)] = {line.split(":")[0].strip(): line.split(":")[1].strip()
                                      for line in m.group(2).strip().split("\n") if ":" in line}

    res["functions"] = [{"name": m.group(1), "params": m.group(2).split(","), "body": m.group(3)}
                        for m in func_def_p.finditer(script)]

    res["function_calls"] = [{"function": m.group(1), "args": m.group(2).split(",")}
                             for m in func_call_p.finditer(script)]

    res["if_blocks"] = [{
        "condition": {"left": m.group(1), "operator": m.group(2), "right": m.group(3)},
        "then": m.group(4),
        "else": m.group(5) if m.group(5) else None
    } for m in if_p.finditer(script)]

    res["for_blocks"] = [{
        "iterator": m.group(1),
        "collection": m.group(2),
        "body": m.group(3)
    } for m in for_p.finditer(script)]

    m = on_error_p.search(script)
    if m:
        res["on_error"] = m.group(1)

    m = loopguard_p.search(script)
    if m:
        res["loopguard"] = {
            "max_depth": int(m.group(1)),
            "allow_repeat": m.group(2).lower() == "true"
        }

    return res

parsed = parse_tags(script)
print(json.dumps(parsed, indent=2))
