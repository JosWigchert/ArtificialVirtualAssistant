import re

TYPE_MAPPING = {
    "str": "string",
    "int": "integer",
    "float": "float",
    "bool": "bool",
    "list": "list",
    "dict": "dict",
    "tuple": "tuple",
    "set": "set",
}


def parse_docstring(function: callable):
    if function.__doc__ is None:
        print("No docstring found")
        return None

    function_object = {}
    function_object["name"] = function.__name__

    docstring = function.__doc__

    # Define the regex pattern
    full_pattern = (
        r"(.+)\s*(?:Parameters:\s*((?:\s*.+:.+\s)*))?\s*(?:Returns:\s*((?:\s*.+:.*)*))?"
    )

    prop_pattern = r"(\w+) \((.+)\):\s*(.+)"
    return_pattern = r"\s*(.+):\s*(.+)"

    # Find the match
    match = re.search(full_pattern, docstring, re.MULTILINE)
    matches = match.groups()

    description = matches[0].strip() if matches[0] else None
    function_object["description"] = description

    parameters = matches[1].strip() if matches[1] else None
    param_dict = {}
    param_dict["type"] = "object"
    param_dict["properties"] = {}
    if parameters:
        required = []
        prop_dict = {}

        for prop_match in re.findall(prop_pattern, parameters):
            enum = re.match(r"\[(.*)\]", prop_match[1])
            prop = {}
            if enum:
                prop["type"] = "string"
                prop["enum"] = (
                    enum.group(1).replace('"', "").replace(" ", "").split(",")
                )
                prop["description"] = prop_match[2]
            else:
                if not prop_match[1] in TYPE_MAPPING:
                    prop["type"] = "object"
                else:
                    prop["type"] = TYPE_MAPPING[prop_match[1]]
                prop["description"] = prop_match[2]

            prop_dict[prop_match[0]] = prop
            if "optional" not in prop_match[1]:
                required.append(prop_match[0])

            param_dict["properties"][prop_match[0]] = prop

        param_dict["required"] = required
    function_object["parameters"] = param_dict

    # returns = matches[2].strip() if matches[2] else None
    # if returns:
    #     return_dict = {}

    #     ret = re.match(return_pattern, returns)
    #     if ret:
    #         return_dict["type"] = ret.group(1)
    #         return_dict["description"] = ret.group(2)
    #         function_object["return"] = return_dict

    return function_object
