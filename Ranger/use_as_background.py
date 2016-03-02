class use_as_background(Command):
    """:use_as_background

    Set current highlighted image as the background.
    """

    def execute(self):
        from mimetypes import guess_type
        from subprocess import call, PIPE

        if self.rest(1):
            self.fm.notify("Error: use_as_background takes no arguments!",
                    bad=True)
            return

        cf = self.fm.thisfile
        if not cf:
            self.fm.notify("Error: no file selected", bad=True)

        cwf = str(cf)
        mime, _ = guess_type(cwf)
        if not ("jpeg" in mime or "png" in mime):
            self.fm.notify("Error: file is not a image", bad=True)
            return

        cmd = ["feh", "--bg-scale", cwf]
        call(cmd, stdout=PIPE, stderr=PIPE)
