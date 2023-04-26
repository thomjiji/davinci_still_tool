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
append_to_timeline_id = "Append clips to timeline"
mismatched_resolution_handling_id = "Handling mismatched resolution"
date_group_for_clips_appending_id = (
    "Date group (e.g.. DAY_001_20230401) for appending clips to timeline by "
    "Scene and Shot"
)
clear_message_id = "Clear messages"
message_tree_id = "Message tree"

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
                        "Weight": 2.3,
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
                        "Weight": 0.2,
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
        ui.HGroup(
            {
                "Spacing": 0,
                "Weight": 0,
            },
            [
                ui.Label(
                    {
                        "Text": "Mismatched Resolution",
                        "Weight": 1,
                    }
                ),
                ui.ComboBox(
                    {
                        "ID": mismatched_resolution_handling_id,
                        "Weight": 1,
                    }
                ),
            ],
        ),
        ui.Button(
            {
                "ID": create_timeline_id,
                "Text": "Create Timeline",
                "Weight": 0,
            }
        ),
    ],
)

append_clips_timeline_by_scene_shot_area = ui.VGroup(
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
                        "Text": "Date Group",
                        "Weight": 1,
                    }
                ),
                ui.ComboBox(
                    {
                        "ID": date_group_for_clips_appending_id,
                        "Weight": 2.2,
                    }
                ),
            ],
        ),
        ui.Button(
            {
                "ID": append_to_timeline_id,
                "Text": "Append Clips to Timeline By Scene and Shot",
                "Weight": 0,
            }
        ),
    ],
)

message_tree_area = ui.VGroup(
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
                        "Text": "Messages",
                        "Weight": 0,
                        "Alignment": {
                            "AlignRight": True,
                            "AlignVCenter": True,
                        },
                    },
                ),
                ui.HGap(),
                ui.Button(
                    {
                        "ID": clear_message_id,
                        "Text": "Clear",
                        "Weight": 1,
                    }
                ),
            ],
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
            ui.VGap(1),
            append_clips_timeline_by_scene_shot_area,
            ui.Label(
                {
                    "StyleSheet": "max-height: 1px; background-color: rgb(10,"
                    "10,10)",
                }
            ),
            message_tree_area,
            ui.VGap(1),
            ui.Tree(
                {
                    "ID": message_tree_id,
                    "Weight": 1,
                    "AlternatingRowColors": True,
                    "HeaderHidden": True,
                    "SelectionMode": "ExtendedSelection",
                    "AutoScroll": True,
                    "SortingEnabled": False,
                    "TabKeyNavigation": True,
                }
            ),
        ],
    ),
)

mismatched_resolution_handling = [
    "Scale full frame with crop",
    "Center crop with no resizing",
    "Scale entire image to fit",
    "Stretch full frame with crop",
]


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

    if (
        itm[mismatched_resolution_handling_id].CurrentText
        == "Scale full frame with crop"
    ):
        current_timeline.SetSetting(
            "timelineInputResMismatchBehavior", "scaleToCrop"
        )
    elif (
        itm[mismatched_resolution_handling_id].CurrentText
        == "Center crop with no resizing"
    ):
        current_timeline.SetSetting(
            "timelineInputResMismatchBehavior", "centerCrop"
        )
    elif (
        itm[mismatched_resolution_handling_id].CurrentText
        == "Scale entire image to fit"
    ):
        current_timeline.SetSetting(
            "timelineInputResMismatchBehavior", "scaleToFit"
        )
    else:
        current_timeline.SetSetting(
            "timelineInputResMismatchBehavior", "stretch"
        )

        return current_timeline.SetSetting("timelineFrameRate", str(24))


def get_clips_in_date_group_source_folder(date_group: str) -> list:
    source_clip_list = []

    date_group_folder_structure = get_subfolder_by_name(
        date_group
    ).GetSubFolderList()

    for folder in date_group_folder_structure:
        if folder.GetName() == "Source":
            for each_video_reel in folder.GetSubFolderList():
                reel_clips = each_video_reel.GetClipList()
                for clip in reel_clips:
                    source_clip_list.append(clip)

    return source_clip_list


def get_clips_by_clip_color(date_group: str, clip_color: str) -> list:
    source_clip_list = get_clips_in_date_group_source_folder(date_group)
    return [
        clip
        for clip in source_clip_list
        if clip.GetClipProperty("Clip Color") == clip_color
    ]


def append_to_timeline(date_group: str):
    for scene in get_scene(date_group, "Pink"):
        current_scene_clips: list = get_clips_by_scene(
            date_group, "Pink", scene
        )

        def key_func(x):
            try:
                return int(x.GetClipProperty("Shot"))
            except ValueError:
                return float("inf")

        sorted_clips = sorted(
            current_scene_clips,
            key=key_func,
            reverse=False,
        )
        sorted_shot = [clip.GetClipProperty("Shot") for clip in sorted_clips]
        print(sorted_shot)
        media_pool.AppendToTimeline(sorted_clips)


def get_scene(date_group: str, clip_color: str) -> list:
    scene_list = []
    for clip in get_clips_by_clip_color(date_group, clip_color):
        scene_list.append(clip.GetClipProperty("Scene"))
    return sorted(set(scene_list))


def get_clips_by_scene(date_group: str, clip_color: str, scene: str) -> list:
    return [
        clip
        for clip in get_clips_by_clip_color(date_group, clip_color)
        if clip.GetClipProperty("Scene") == scene
    ]


# Get items of the UI
itm = win.GetItems()

itm[mismatched_resolution_handling_id].AddItems(mismatched_resolution_handling)
date_groups = [
    subfolder.GetName()
    for subfolder in root_folder.GetSubFolderList()
    if not subfolder.GetName().startswith("_")
]
itm[date_group_for_clips_appending_id].AddItems(date_groups)


# Events handlers
def on_close(ev):
    """Close the window."""
    dispatcher.ExitLoop()


def on_click_create_timeline_button(ev):
    width = itm[timeline_resolution_width_id].Text
    height = itm[timeline_resolution_height_id].Text
    name = itm[timeline_name_id].Text
    create_timeline(name, width, height)


def on_click_append_to_timeline_button(ev):
    date_group = itm[date_group_for_clips_appending_id].CurrentText
    append_to_timeline(date_group)
    for scene in get_scene(date_group, "Pink"):
        row = itm[message_tree_id].NewItem()
        row.Text[0] = f'Add "Scene {scene}" into timeline.'
        itm[message_tree_id].AddTopLevelItem(row)


def on_click_clear_messages_button(ev):
    itm[message_tree_id].Clear()


# Assign events handlers
win.On.myWindow.Close = on_close
win.On[create_timeline_id].Clicked = on_click_create_timeline_button
win.On[append_to_timeline_id].Clicked = on_click_append_to_timeline_button
win.On[clear_message_id].Clicked = on_click_clear_messages_button

if __name__ == "__main__":
    win.Show()
    dispatcher.RunLoop()