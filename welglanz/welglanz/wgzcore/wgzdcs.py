"""WGZ Dataclasses."""

from dataclasses import dataclass

from typing import Any


# WGZ password mask dataclass.
@dataclass
class WgzPassword:
    """A data class to represent a password mask."""

    password: bool
    """Indicates whether the mask is enabled"""

    mask: str
    """The mask character(s)."""

# Utility for creating custom password mask.
def wgz_new_password(mask: str) -> WgzPassword:
    """Create a WgzPassword object with the given mask."""
    return WgzPassword(True, mask)

# WGZ Prompt dataclass.
@dataclass
class WgzPromptReturn:
    """A data class to represent the return value of a WGZ prompt."""

    interrupted: bool
    """Indicates whether the prompt was interrupted by a KeyboardInterrupt."""

    validated: bool
    """Indicates whether the input was validated by the validator function."""

    ureturn: str
    """The user input received from the prompt."""

# WGZ Selectable icons dataclass.
@dataclass
class WgzSelectableIcon:
    """A data class for customizing selectables icon."""

    icon_default: str
    """The default icon when selectable is not selected."""

    icon_selected: str
    """The selected icon when selectable is selected."""

# Utility for creating custom selectable icons.
def wgz_new_selectable_icon(icon_default: str, icon_selected: str) -> WgzSelectableIcon:
    """Create a WgzSelectableIcon object with the given icons."""
    return WgzSelectableIcon(icon_default, icon_selected)

# WGZ Selectable dataclasses.
@dataclass
class WgzSelectable:
    """A data class to represent a selectable item."""

    selectable_text: str
    """The text of the selectable item."""

    selectable_id: str
    """The ID of the selectable item."""

    selectable_hint: str=None
    """The hint of the selectable item (on hover on the selectable)."""

@dataclass
class WgzSelectReturn:
    """A data class to represent the return value of selection."""

    interrupted: bool
    """Indicates whether the selecting option was interrupted by a KeyboardInterrupt."""

    selected_id: str
    """The ID of the selected selectable."""

@dataclass
class WgzMultiselectReturn:
    """A data class to represent the return value of a multiselect."""

    interrupted: bool
    """Indicates whether the multiselect option was interrupted by a KeyboardInterrupt."""

    selected_ids: tuple[str]
    """The IDs of the selected selectables."""

# WGZ Confirm dataclasses.
@dataclass
class WgzConfirmText:
    """A data class for customizing confirm text."""

    yes: str
    """The text for the 'yes'/True option."""

    no: str
    """The text for the 'no'/False option."""

# Utility for creating custom confirm text.
def wgz_new_confirm_text(yes: str, no: str) -> WgzConfirmText:
    """Create a WgzConfirmText object with the given confirm text."""
    return WgzConfirmText(yes, no)

# WGZ Confirm dialog return.
@dataclass
class WgzConfirmReturn:
    """A data class to represent the return value of a confirm dialog."""

    interrupted: bool
    """Indicates whether the confirm dialog was interrupted by a KeyboardInterrupt."""

    confirmed: bool
    """Indicates whether the user confirmed the dialog."""

# WGZ Spinner dataclasses.
@dataclass
class WgzSpinnerIcon:
    """A data class for customizing spinner icon."""

    name: str
    """Spinner icon name."""

    icon: tuple[str]
    """Spinner icon."""

# Utility for creating custom spinner icon.
def wgz_new_spinner_icon(name: str, *icon: str) -> WgzSpinnerIcon:
    """Create a WgzSpinnerIcon object with the given icon."""
    return WgzSpinnerIcon(name, icon)

# WGZ Stop signal dataclass.
@dataclass
class WgzStopSignal:
    """WGZ stop signal dataclass."""

    stop_required: bool=False
    """Is stop required?"""

# WGZ Data dataclass
@dataclass
class WgzData:
    """WGZ dataclass used for sharing data between WGZ and function."""

    data: Any=None

# WGZ Progress bar value dataclass.
@dataclass
class WgzPBValueLink:
    """WGZ datacalss used for sharing a progress bar value between WGZ and function."""

    value: float
