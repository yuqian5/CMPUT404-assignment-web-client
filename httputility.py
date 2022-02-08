def parse_response(resp):
    header, body = resp.split("\r\n\r\n")
    parts = header.split("\r\n")

    result = {}

    # get code
    code = get_response_code(parts[0])
    result["code"] = int(code[0])
    result["code message"] = code[1]
    parts.pop(0)

    # get body
    result["body"] = body

    # parse the rest of the headers
    for i in parts:
        (name, value) = i.split(": ", 1)
        result[name] = value

    return result


def get_response_code(part):
    parts = part.split(" ")

    parts.pop(0)

    code = parts.pop(0)
    code_message = " ".join(parts)

    return code, code_message


def args_2_url_encode(args):
    if args is None:
        return ""

    result = ""

    for i in args:
        result += f"{i}={args[i]}&"

    return result[:-1]



