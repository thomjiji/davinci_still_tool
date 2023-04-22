from resolve_init import GetResolve

# Initialize Resolve base object.
resolve = GetResolve()
project = resolve.GetProjectManager().GetCurrentProject()
media_pool = project.GetMediaPool()
root_folder = media_pool.GetRootFolder()
media_storage = resolve.GetMediaStorage()
current_timeline = project.GetCurrentTimeline()

# Initialize the UI
fusion = bmd.scriptapp("Fusion")  # type: ignore
ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)  # type: ignore


# Compose the whole UI
win = dispatcher.AddWindow()


# General functions
def get_subfolder_by_name(subfolder_name: str):
    all_subfolder = root_folder.GetSubFolderList()
    subfolder_dict = {
        subfolder.GetName(): subfolder for subfolder in all_subfolder
    }
    return subfolder_dict.get(subfolder_name, "")


# Get items of the UI
itm = win.GetItems()


# Events handlers
def on_close(ev):
    """Close the window."""
    dispatcher.ExitLoop()


# Assign events handlers
win.On.myWindow.close = on_close


if __name__ == "__main__":
    win.Show()
    dispatcher.RunLoop()
