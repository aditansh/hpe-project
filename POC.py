import json
f = open('kb.json')
data = json.load(f)
for i in data['emp_details']:
    print(i)

data = json.loads(knowledge_base)
 
def call_tool(toolname, command, **kwargs):
    print(f"Calling {toolname} with command {command} and arguments {kwargs}")

def execute_use_case(user_input):
    found = False

    for use_case in data["use_cases"]:
        if use_case["name"].lower() == user_input.lower():
            found = True
            print("Executing use case: {use_case['name']}")
            print("Description: {use_case['description']}")
            for tool in use_case["tools"]:
                toolname = tool["toolname"]
                command = tool["commands"]
                arguments = tool["arguments"]
                print("Calling tool: {toolname}, Command: {command}")
                provided_args = {}
                for arg in arguments:
                    value = input("Enter value for argument '{arg}': ")
                    provided_args[arg] = value
                call_tool(toolname, command, **provided_args)
    if not found:
        print("Use case not found.")

user_input = input("Enter the name of the security-based use case: ")
execute_use_case(user_input)