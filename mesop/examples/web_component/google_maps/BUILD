load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_examples"],
)

py_library(
    name = "google_maps",
    srcs = glob(["*.py"]),
    data = glob(["*.js"]),
    deps = [
        "//mesop",
    ],
)
