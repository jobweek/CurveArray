import bpy  # type: ignore


class CancelError(Exception):

    pass


def ShowMessageBox(title, message, icon):

    def draw(self, _):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
