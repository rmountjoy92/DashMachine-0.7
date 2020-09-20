import os
import toml
import json
from dashmachine.paths import documentation_folder, vs_folder
from vscode_integration.utils import (
    build_type_description,
    build_snippet_body_template,
)


def generate_snippets():
    snippet_json = {}
    snippet_json = class_snippets(
        snippet_json=snippet_json,
        class_name="Card",
        prefill="['${1:card_name}']\n${2}",
        description=(
            "\nReplace card_name with unique string.\n"
            "Only to be used in a dashboard toml file or shared_cards.toml"
        ),
    )
    snippet_json = class_snippets(
        snippet_json=snippet_json,
        class_name="DashboardOptions",
        prefill="[DashboardOptions]\n${1}",
        description="\nOnly to be used in a dashboard toml file.",
    )
    snippet_json = class_snippets(
        snippet_json=snippet_json,
        class_name="Settings",
        prefill="[Settings]\n${1}",
        description="\nOnly to be used in the settings.toml file.",
    )
    snippet_json = class_snippets(
        snippet_json=snippet_json,
        class_name="User",
        prefill="['${1:username}']\n${2}",
        description=(
            "\nReplace username with unique string.\n" "Only to be used in users.toml"
        ),
    )
    snippet_json = utility_snippets(snippet_json)

    with open(
        os.path.join(vs_folder, "ext", "snippets", "snippets.code-snippets"), "w"
    ) as snippets_file:
        snippets_file.write(json.dumps(snippet_json))
    return snippet_json


def class_snippets(snippet_json, class_name, prefill, description):
    class_toml = toml.load(
        os.path.join(documentation_folder, f"{class_name.lower()}.toml")
    )
    snippet_json[class_name] = {}
    snippet_json[class_name]["prefix"] = class_name
    snippet_json[class_name]["body"] = prefill
    snippet_json[class_name][
        "description"
    ] = f"Start a {class_name} object. {description}"

    for property_name, property_dict in class_toml[class_name].items():
        snippet_json = build_snippet_from_property(
            snippet_json=snippet_json,
            classname=class_name,
            property_name=property_name,
            property_dict=property_dict,
        )
    return snippet_json


def utility_snippets(snippet_json):
    utils_toml = toml.load(os.path.join(documentation_folder, "utils.toml"))
    for classname, options in utils_toml.items():
        snippet_json[classname] = {}
        snippet_json[classname]["prefix"] = classname
        snippet_json[classname]["body"] = "{"
        snippet_json[classname][
            "description"
        ] = f"Start a {classname} object. \n\nKEYS:\n"
        key_index = 1
        for key_dict in options["keys"]:
            snippet_json[classname]["body"] += build_snippet_body_template(
                property_name=key_dict["name"],
                property_type=key_dict["type"],
                key_index=key_index,
                before_prefill=key_dict.get("before_prefill"),
                prefill=key_dict.get("prefill"),
            )
            if key_index < len(options["keys"]):
                snippet_json[classname]["body"] += ", "
            snippet_json[classname]["description"] += (
                f"{key_dict['name']}\n"
                f"{key_dict['description']}\n"
                + build_type_description(key_dict["type"], key_dict.items())
                + "\n"
            )
            key_index += 1
        if options.get("shorthand"):
            snippet_json[classname]["description"] += (
                "\n |Shorthand available|\n Simply provide the following:\n"
                f"-{options['shorthand']}-\n"
                "and it will use the defaults for the rest of the keys."
            )
        snippet_json[classname]["body"] += "}"
    return snippet_json


def build_snippet_from_property(
    snippet_json, classname, property_name, property_dict, parent_name=None
):
    prefix_name = f"{classname}.{property_name}"
    if parent_name:
        property_name = f"{parent_name}.{property_name}"
    snippet_json[prefix_name] = {
        "prefix": prefix_name,
        "description": f'{prefix_name} \n{property_dict.get("description", "")} \n\n',
    }
    property_type = property_dict.get("type")

    if property_dict.items():
        snippet_json[prefix_name]["description"] += build_type_description(
            property_type, property_dict.items()
        )

    if property_type == "dict":
        key_index = 1
        body = "{"
        for k, v in property_dict.items():
            if k not in ["type", "description"]:
                body += k + "= ${" + str(key_index) + "}, "
                key_index += 1
        body = body + "}"
        snippet_json[prefix_name]["body"] = f"{property_name} = " + body
    else:
        snippet_json[prefix_name]["body"] = build_snippet_body_template(
            property_name=property_name, property_type=property_type
        )

    if "dict" in property_type:
        for dict_prop_name, dict_prop_dict in property_dict.items():
            if dict_prop_name not in ["type", "description"]:
                snippet_json = build_snippet_from_property(
                    snippet_json=snippet_json,
                    classname=prefix_name,
                    property_name=dict_prop_name,
                    property_dict=dict_prop_dict,
                    parent_name=property_name,
                )

    return snippet_json
