import re


def parse_type_params(type_str: str) -> tuple[str, []]:
    """
    Parse type string and return type name and parameters dict

    Args:
        type_str: Type string like 'DECIMAL(10, 2)' or 'BIGINT(display_width=20)' or VARCHAR(20)

    Returns:
        tuple: (type_name, params_dict)
        e.g.: ('decimal', {'precision': 10, 'scale': 2})
    """
    # Match type name and parameters in parentheses
    match = re.match(r"(\w+)\((.*)\)", type_str)
    if not match:
        return type_str, {}

    type_name = match.group(1)
    params_str = match.group(2)

    # Parse parameters
    params = []
    if params_str:
        # Split multiple parameters
        param_pairs = params_str.split(",")
        for pair in param_pairs:
            params.append(pair)

    return type_name, params
