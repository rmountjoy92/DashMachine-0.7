toml_docs_path = "https://toml.io/en/v1.0.0-rc.1"
moz_docs_path = "https://developer.mozilla.org/en-US/docs/Web/"


def build_type_description(property_type, dict_items=None):
    description = f"[{property_type}] "

    # TOML TYPES
    if "list" in property_type:
        description += f"<toml list> : {toml_docs_path}#array>"

    if property_type == "string":
        description += f"<toml string> : {toml_docs_path}#string"

    if property_type == "int":
        description += f"<toml integer> : {toml_docs_path}#integer"

    if property_type == "bool":
        description += f"<toml boolean> : {toml_docs_path}#boolean"

    if property_type == "dict":
        description += f"<toml inline table> : {toml_docs_path}#inline-table"
        description += "\n\nKEYS:\n"
        for k, v in dict_items:
            if k not in ["type", "description"]:
                description += (
                    f"| {k} | {v.get('description', k)} | "
                    f"{build_type_description(v['type'], dict_items=v.items())} | \n\n"
                )

    # CSS TYPES
    if property_type == "color":
        description += f"<css color> : {moz_docs_path}CSS/color_value"

    if property_type == "size":
        description += f"<css size> : {moz_docs_path}CSS/@page/size"

    if property_type == "classes":
        description += f"<css class selectors> : {moz_docs_path}CSS/Class_selectors"

    if property_type == "css":
        description += f"<css code> : {moz_docs_path}CSS"

    # DashMachine Types
    if property_type == "Image":
        description += f"<DashMachine Image Object> "
    if property_type == "Onpress":
        description += f"<DashMachine Onpress Object> "
    if property_type == "Action":
        description += f"<DashMachine Action Object> "

    return description + "\n"


def build_snippet_body_template(
    property_name, property_type, key_index=1, before_prefill=None, prefill=None
):
    body = f"{property_name} = "

    if property_type in [
        "string",
        "color",
        "size",
        "classes",
        "css",
        "string or dict",
        "Image or dict",
    ]:
        quote_template = True
    else:
        quote_template = False

    if "list" in property_type:
        if "<string>" in property_type or "list or" in property_type:
            body += "['${1}']"
        elif "<int>" in property_type:
            body += "[${1}]"
        else:
            list_item_type = property_type[
                property_type.find("<") + 1 : property_type.find(">")
            ]
            body += "[\n    ${1:" + list_item_type + "},\n]"
        return body

    if property_type == "bool" and not prefill:
        prefill = "true"

    if property_type == "color" and not prefill:
        before_prefill = "#"
        prefill = "000000"

    if property_type == "size" and not prefill:
        prefill = "64px"

    if property_type == "css" and not prefill:
        body += "'${1:}: ${2};'"
        return body

    if property_type == "Onpress":
        prefill = "Onpress"

    if property_type == "Image":
        prefill = "Image"

    if property_type == "Action":
        prefill = "Action"

    if quote_template:
        body += "'"
    if before_prefill:
        body += before_prefill
    body += "${"
    if prefill:
        if isinstance(prefill, str):
            body += f"{key_index}:{prefill}"
        else:
            prefill = ",".join(prefill)
            body += f"{key_index}|{prefill}|"
    else:
        body += f"{key_index}"
    body += "}"
    if quote_template:
        body += "'"
    return body
