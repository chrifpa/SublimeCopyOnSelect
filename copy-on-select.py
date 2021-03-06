import sublime
import sublime_plugin
import functools


class CopyOnSelectCommand(sublime_plugin.EventListener):

    @property
    def delay(self):
        settings = sublime.load_settings("CopyOnSelect.sublime-settings")
        if settings:
            delay = settings.get("delay", 1000)
            try:
                return int(delay)
            except:
                pass
        return 1000

    # number of pending calls to handle_timeout
    pending = 0

    def handle_timeout(self, view):
        self.pending = self.pending - 1
        if self.pending == 0:
            # There are no more queued up calls to handle_timeout, so it must have
            # been {delay}ms since the last modification
            self.on_idle(view)

    def on_selection_modified(self, view):
        self.pending = self.pending + 1
        # Ask for handle_timeout to be called in DELAY ms
        sublime.set_timeout(functools.partial(self.handle_timeout, view), self.delay)

    def on_idle(self, view):
        string = ""
        for region in view.sel():
            if not region.empty():
                string += view.substr(region)
        if string != "":
            sublime.set_clipboard(string)
