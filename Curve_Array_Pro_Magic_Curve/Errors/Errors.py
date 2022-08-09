import bpy  # type: ignore


class CancelError(Exception):

    pass


def show_message_box(title, message, icon):

    def draw(self, _):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def runtime_info(self, info):

    self.report({'INFO'}, info)
