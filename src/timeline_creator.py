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

# Declare UI elements ID
create_timeline_id = "Create timeline"
timeline_resolution_width_id = "Timeline resolution (width)"
timeline_resolution_height_id = "Timeline resolution (height)"
timeline_name_id = "Timeline name"

timeline_creating_input_area = ui.VGroup(
    {
        "Spacing": 5,
        "Weight": 0,
    },
    [
        ui.HGroup(
            {
                "Spacing": 5,
                "Weight": 0,
            },
            [
                ui.Label(
                    {
                        "Text": "Timeline Name",
                        "Weight": 1,
                    },
                ),
                ui.LineEdit(
                    {
                        "ID": timeline_name_id,
                        "Weight": 1,
                    }
                ),
            ],
        ),
        ui.HGroup(
            {
                "Spacing": 0,
                "Weight": 0,
            },
            [
                ui.Label(
                    {
                        "Text": "Resolution",
                        "Weight": 1,
                    }
                ),
                ui.LineEdit(
                    {
                        "ID": timeline_resolution_width_id,
                        "Weight": 1,
                        "Alignment": {
                            "AlignCenter": True,
                        },
                    },
                ),
                ui.Label(
                    {
                        "Text": "x",
                        "Alignment": {
                            "AlignCenter": True,
                        },
                        "Weight": 0,
                    }
                ),
                ui.LineEdit(
                    {
                        "ID": timeline_resolution_height_id,
                        "Weight": 1,
                        "Alignment": {
                            "AlignCenter": True,
                        },
                    },
                ),
            ],
        ),
        ui.Button(
            {
                "ID": create_timeline_id,
                "Text": "Create",
                "Weight": 0,
            }
        ),
    ],
)

# Compose the whole UI
win = dispatcher.AddWindow(
    {
        "ID": "myWindow",
        "Geometry": [
            750,
            200,
            400,
            500,
        ],
        "WindowTitle": "Timeline Creator",
    },
    ui.VGroup(
        {
            "Spacing": 5,
            "Weight": 0,
        },
        [
            timeline_creating_input_area,
        ],
    ),
)


# General functions
def get_subfolder_by_name(subfolder_name: str):
    all_subfolder = root_folder.GetSubFolderList()
    subfolder_dict = {
        subfolder.GetName(): subfolder for subfolder in all_subfolder
    }
    return subfolder_dict.get(subfolder_name, "")


def create_timeline(timeline_name: str, width: int, height: int):
    media_pool.CreateEmptyTimeline(timeline_name)
    current_timeline = project.GetCurrentTimeline()
    current_timeline.SetSetting("useCustomSettings", "1")
    current_timeline.SetSetting("timelineResolutionWidth", str(width))
    current_timeline.SetSetting("timelineResolutionHeight", str(height))
    current_timeline.SetSetting(
        "timelineInputResMismatchBehavior", "scaleToCrop"
    )
    return current_timeline.SetSetting("timelineFrameRate", str(24))


def get_video_clips_in_date_group_source_folder(date_group: str) -> list:
    source_clip_list = []

    date_group_folder_structure = get_subfolder_by_name(
        date_group
    ).GetSubFolderList()  # type: ignore

    for folder in date_group_folder_structure:
        if folder.GetName() == "Source":
            for each_video_reel in folder.GetSubFolderList():
                reel_clips = each_video_reel.GetClipList()
                for clip in reel_clips:
                    source_clip_list.append(clip)

    return source_clip_list


def get_clips_by_clip_color(date_group: str, clip_color: str) -> list:
    source_clip_list = get_video_clips_in_date_group_source_folder(date_group)
    return [
        clip
        for clip in source_clip_list
        if clip.GetClipProperty("Clip Color") == clip_color
    ]


def append_to_timeline(clip_list: list):
    pass


def get_scene(date_group: str, clip_color: str) -> list:
    scene_list = []
    for clip in get_clips_by_clip_color(date_group, clip_color):
        scene_list.append(clip.GetClipProperty("Scene"))
    return scene_list


def get_clips_by_scene(date_group: str, clip_color: str, scene: str) -> list:
    return [
        clip
        for clip in get_clips_by_clip_color(date_group, clip_color)
        if clip.GetClipProperty("Scene") == scene
    ]


# Get items of the UI
itm = win.GetItems()


# Events handlers
def on_close(ev):
    """Close the window."""
    dispatcher.ExitLoop()


def on_click_create_timeline_button(ev):
    width = itm[timeline_resolution_width_id].Text
    height = itm[timeline_resolution_height_id].Text
    name = itm[timeline_name_id].Text
    create_timeline(name, width, height)


# Assign events handlers
win.On.myWindow.Close = on_close
win.On[create_timeline_id].Clicked = on_click_create_timeline_button

if __name__ == "__main__":
    win.Show()
    dispatcher.RunLoop()
