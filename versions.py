def get_newer_version(version1: str, version2: str) -> str:
    """
    Compare two version numbers and return the newer one.

    Args:
        version1: First version number as string
        version2: Second version number as string

    Returns:
        The newer version number
    """
    # Convert version strings to comparable tuples
    def parse_version(version):
        # Split by dots first
        parts = []
        for part in version.split('.'):
            if part.isnumeric():
                parts.append((int(part), part))
            else:
                # Check for environment indicators only if non-numeric
                for sep in ['-', '_']:
                    if sep in part:
                        base, env = part.split(sep, 1)
                        if base.isnumeric():
                            parts.append((int(base), base))
                        else:
                            parts.append((0, base))
                        # Environment priority
                        env = env.lower()
                        env_value = {"dev": 1, "qa": 2, "stage": 3, "preprod": 4, "prod": 5}.get(env, 0)
                        parts.append((env_value, env))
                        break
                else:
                    # No separator found
                    parts.append((0, part))
        return parts

    v1_parts = parse_version(version1)
    v2_parts = parse_version(version2)

    # Simple comparison of the tuples
    return version1 if v1_parts >= v2_parts else version2


assert get_newer_version("1.2.3", "1.3.0") == "1.3.0"
assert get_newer_version("2.0.1", "2.1") == "2.1"
assert get_newer_version("2.0", "10.0") == "10.0"
assert get_newer_version("1.a", "1.b") == "1.b"
assert get_newer_version("1.0-qa", "1.0-prod") == "1.0-prod"