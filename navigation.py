"""
Single-window navigation helpers.

Every screen used to open in its own pop-up window (tk.Toplevel), which is
why you saw several windows at once. Now each screen is a `Page` (a Frame)
shown inside one `PageHost` in the main window, like pages of a website.

- Page      : drop-in replacement for tk.Toplevel(parent) in the screen classes
- PageHost  : the area of the main window where the current page is displayed
"""

import tkinter as tk


class PageHost(tk.Frame):
    """Holds exactly one page at a time."""

    def __init__(self, master, on_close=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_close = on_close      # called when a page closes itself
        self._closing = False

    def clear(self):
        """Remove whatever page is currently shown."""
        for child in list(self.winfo_children()):
            if isinstance(child, Page):
                child.destroy_silently()
            else:
                child.destroy()

    def page_closed(self):
        if self.on_close and not self._closing:
            self.on_close()

    def destroy(self):
        self._closing = True
        super().destroy()


class Page(tk.Frame):
    """
    A screen that lives inside the main window.

    It accepts the window-style calls the old screens make (title, geometry,
    minsize, resizable, protocol) and ignores them, so those screens keep working.

    Calling destroy() (the old "Close" buttons) closes the page and returns
    to the home screen. Use destroy_silently() to move to another page yourself.
    """

    def __init__(self, host, bg=None):
        super().__init__(host)
        if bg:
            self.configure(bg=bg)
        self.pack(fill="both", expand=True)

    # ---- window-style calls that no longer apply ----
    def title(self, *args, **kwargs):
        pass

    def geometry(self, *args, **kwargs):
        pass

    def minsize(self, *args, **kwargs):
        pass

    def resizable(self, *args, **kwargs):
        pass

    def protocol(self, *args, **kwargs):
        pass

    # ---- closing ----
    def _teardown(self):
        # Remove key / mouse-wheel bindings this page added to the whole app
        try:
            self.winfo_toplevel().unbind("<Return>")
            self.unbind_all("<MouseWheel>")
        except tk.TclError:
            pass

    def destroy_silently(self):
        """Close this page without navigating anywhere."""
        self._teardown()
        super().destroy()

    def destroy(self):
        """Close this page and go back to the home screen."""
        host = self.master
        self._teardown()
        super().destroy()
        if isinstance(host, PageHost):
            host.page_closed()
