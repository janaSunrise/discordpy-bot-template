import importlib
import inspect
import pkgutil
import types
import typing as t

from bot import cogs


def get_module_name(name: str) -> str:
    """Get the cog name from the module."""
    return name.split(".")[-1]


def is_a_cog(module: types.ModuleType) -> bool:
    """Check if the module has a setup function, which implies it's a cog."""
    imported = importlib.import_module(module.name)
    return inspect.isfunction(getattr(imported, "setup", None))


def get_modules_list(
    package: types.ModuleType, check: t.Optional[types.FunctionType] = None
) -> t.List[str]:
    """Get the list of the submodules from the specified package."""
    modules = []

    for submodule in pkgutil.walk_packages(package.__path__, f"{package.__name__}."):
        if get_module_name(submodule.name).startswith("_"):
            continue

        if check and not check(submodule):
            continue

        modules.append(submodule.name)

    return modules


COGS = get_modules_list(cogs, check=is_a_cog)
