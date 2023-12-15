from typing import Any, Callable, Literal

from pydantic import validate_arguments

import mesop.components.button.button_pb2 as button_pb
from mesop.component_helpers import (
  handler_type,
  insert_composite_component,
)
from mesop.events import ClickEvent


@validate_arguments
def button(
  *,
  key: str | None = None,
  color: str = "",
  disable_ripple: bool = False,
  disabled: bool = False,
  aria_disabled: bool = False,
  on_click: Callable[[ClickEvent], Any] | None = None,
  variant: Literal[
    "mat-button", "mat-raised-button", "mat-flat-button", "mat-stroked-button"
  ] = "mat-button",
):
  """
  TODO_doc_string
  """
  return insert_composite_component(
    key=key,
    type_name="button",
    proto=button_pb.ButtonType(
      color=color,
      disable_ripple=disable_ripple,
      disabled=disabled,
      aria_disabled=aria_disabled,
      on_click_handler_id=handler_type(on_click) if on_click else "",
      variant_index=_get_variant_index(variant),
    ),
  )


def _get_variant_index(variant: str) -> int:
  if variant == "mat-button":
    return 0
  if variant == "mat-raised-button":
    return 1
  if variant == "mat-flat-button":
    return 2
  if variant == "mat-stroked-button":
    return 3
  raise Exception("Unexpected variant: " + variant)