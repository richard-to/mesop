load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "mesop",
    srcs = [
        "__init__.py",
        "api.py",
    ],
    deps = [
        # REF(//scripts/gen_component.py):insert_component_import
        "//mesop/components/markdown:py",
        "//mesop/components/text_input:py",
        "//mesop/components/box:py",
        "//mesop/components",
        "//mesop/components/button:py",
        "//mesop/components/checkbox:py",
        "//mesop/components/text:py",
        "//mesop/event_handler",
        "//mesop/events",
        "//mesop/features",
        "//mesop/server",
    ],
)