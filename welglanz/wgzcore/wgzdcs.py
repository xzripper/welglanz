"""WGZ Dataclasses."""

from welglanz.wgzcore import _wgz_ensure_char

from dataclasses import dataclass

from typing import Union, Any


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
    _wgz_ensure_char(mask)

    return WgzPassword(True, mask)

# WGZ Prompt dataclass.
@dataclass
class WgzPromptReturn:
    """A data class to represent the return value of a WGZ prompt."""

    interrupted: bool
    """Indicates whether the prompt was interrupted by a KeyboardInterrupt."""

    validated: bool
    """Indicates whether the input was validated by the validator function."""

    p_return: str
    """An output received from a prompt."""

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
    _wgz_ensure_char(icon_default)
    _wgz_ensure_char(icon_selected)

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

    dreturn: bool
    """An index of a choice in a dialog that ranging between 0 and 1."""

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
    (_wgz_ensure_char(i) for i in icon)

    return WgzSpinnerIcon(name, icon)

# WGZ Interruption signal dataclass.
@dataclass
class WgzInterruptionSignal:
    """A data class to represent interruption signal."""

    interrupted: bool=False
    """Is interrupted?"""

    inner_interruption: bool=None
    """Manual interruption data slot."""

    def interrupt_inner_state(self) -> None:
        """Make an immediate inner interruption."""
        self.inner_interruption = True

# WGZ Data dataclass
@dataclass
class WgzData:
    """A data class for sharing data between WGZ and a callback."""

    data1: Any=None
    """First data slot."""

    data2: Any=None
    """Second data slot."""

    data3: Any=None
    """Third data slot."""

# WGZ Progress bar dataclass.
@dataclass
class WgzProgressBarData:
    """A data class to represent progress bar data."""

    progress: int=0
    """Progress value."""

    str_status: str=None
    """Progress bar status in a string."""

    def set_progress(self, n_progress: Union[int, float]) -> None:
        """Set bar's progress (automatically converts the progress to an integer)."""
        self.progress = int(n_progress)

    def set_status(self, repr_status: Any) -> None:
        """Set bar's status (automatically converts the status to a string)."""
        self.str_status = str(repr_status)
