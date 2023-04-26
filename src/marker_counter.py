from resolve_init import GetResolve
from dftt_timecode import DfttTimecode

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
outputPathID = "Output Path"
testClickID = "Test Click"
messageTreeID = "Message Tree"
countMarkerID = "Count Marker"
browseOutputFileManagerID = "Browse File Manager"
markerColorForRemovalID = "Marker color for removal"
markerColorForCountingID = "Marker color for counting"
deleteMarkersByColorID = "Delete Marker By Color"
timelinesID = "Timelines in the mediapool"
copyMarkersFromSpecifiedTimelineID = "Copy markers from specified timeline"
markerCountDisplayID = "Display marker counts"
undoCopyAndPasteMarkersID = "Undo copy and paste markers"
clearMessagesID = "Clear messages"
start_timecode_id = "Start timecode for markers copy and pasting"
end_timecode_id = "End timecode for markers copy and pasting"
update_start_and_end_frame_id = (
    "Update start and end timecode of current timeline"
)

# UI components
output_path_select_component = ui.HGroup(
    {
        "Spacing": 5,
        "Weight": 0,
    },
    [
        ui.Label(
            {
                "Text": "Output Path",
                "Weight": 0,
                "Alignment": {
                    "AlignRight": True,
                    "AlignVCenter": True,
                },
            },
        ),
        ui.LineEdit(
            {
                "ID": outputPathID,
                "ClearButtonEnabled": True,
            }
        ),
        ui.Button(
            {
                "ID": browseOutputFileManagerID,
                "Text": "Browse",
                "Weight": 0,
            }
        ),
    ],
)

marker_number_display_area = ui.HGroup(
    {
        "Spacing": 5,
        "Weight": 0,
    },
    [
        ui.Label(
            {
                "Text": "Marker Number",
                "Weight": 1,
            }
        ),
        ui.LineEdit(
            {
                "ID": markerCountDisplayID,
                "Weight": 1,
                "Text": "",
                "ReadOnly": True,
            }
        ),
    ],
)

count_marker_by_color_area = ui.HGroup(
    {
        "Spacing": 5,
        "Weight": 0,
    },
    [
        ui.Label(
            {
                "Text": "Count Marker By Color",
                "Weight": 1,
            }
        ),
        ui.ComboBox({"ID": markerColorForCountingID, "Weight": 1}),
    ],
)

count_marker_button = ui.HGroup(
    {
        "Spacing": 5,
        "Weight": 0,
    },
    [
        ui.Button(
            {
                "ID": countMarkerID,
                "Text": "Count",
                "Weight": 1,
                "AlignRight": True,
            }
        ),
    ],
)

remove_marker_by_color_area = ui.HGroup(
    {
        "Spacing": 5,
        "Weight": 0,
    },
    [
        ui.Label(
            {
                "Text": "Remove Marker By Color",
                "Weight": 1,
            }
        ),
        ui.ComboBox({"ID": markerColorForRemovalID, "Weight": 1}),
    ],
)

remove_marker_button = ui.HGroup(
    {
        "Spacing": 5,
        "Weight": 0,
    },
    [
        ui.Button(
            {
                "ID": deleteMarkersByColorID,
                "Text": "Remove",
                "Weight": 1,
            }
        ),
    ],
)

copy_markers_from_area = ui.VGroup(
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
                        "Text": "Copy Markers From",
                        "Weight": 1,
                    }
                ),
                ui.ComboBox(
                    {
                        "ID": timelinesID,
                        "Weight": 1,
                    }
                ),
            ],
        ),
        ui.HGroup(
            {
                "Spacing": 5,
                "Weight": 0,
            },
            [
                ui.Label(
                    {
                        "Text": "In",
                        "Weight": 1,
                        "Alignment": {
                            "AlignRight": True,
                        },
                    }
                ),
                # ui.HGap(),
                ui.LineEdit(
                    {
                        "ID": start_timecode_id,
                        "Weight": 1.1,
                        "PlaceholderText": "01:00:00:00",
                        "Alignment": {
                            "AlignHCenter": True,
                        },
                    }
                ),
                # ui.HGap(0.1),
                ui.Label(
                    {
                        "Text": "to",
                        "Weight": 0.1,
                        "Alignment": {
                            "AlignHCenter": True,
                        },
                    }
                ),
                # ui.HGap(0.1),
                ui.LineEdit(
                    {
                        "ID": end_timecode_id,
                        "Weight": 1.1,
                        "PlaceholderText": "01:00:10:00",
                        "Alignment": {
                            "AlignHCenter": True,
                        },
                    }
                ),
            ],
        ),
        ui.HGroup(
            {
                "Spacing": 5,
                "Weight": 0,
            },
            [
                ui.Button(
                    {
                        "ID": copyMarkersFromSpecifiedTimelineID,
                        "Text": "Copy and Paste",
                        "Weight": 1,
                    }
                ),
                ui.Button(
                    {
                        "ID": undoCopyAndPasteMarkersID,
                        "Text": "Undo",
                        "Weight": 1,
                    }
                ),
                ui.Button(
                    {
                        "ID": update_start_and_end_frame_id,
                        "Text": "Update Timecode",
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
        "WindowTitle": "DaVinci Still & Marker Tool",
    },
    ui.VGroup(
        {
            "Spacing": 5,
            "Weight": 0,
        },
        [
            output_path_select_component,
            #
            ui.VGap(1),
            marker_number_display_area,
            count_marker_by_color_area,
            count_marker_button,
            #
            ui.VGap(1),
            remove_marker_by_color_area,
            remove_marker_button,
            #
            ui.VGap(1),
            copy_markers_from_area,
            #
            ui.Label(
                {
                    "StyleSheet": "max-height: 1px; background-color: rgb(10,"
                    "10,10)",
                }
            ),
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
                            "ID": clearMessagesID,
                            "Text": "Clear",
                            "Weight": 1,
                        }
                    ),
                ],
            ),
            ui.Tree(
                {
                    "ID": messageTreeID,
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

marker_colors = [
    "Blue",
    "Cyan",
    "Green",
    "Yellow",
    "Red",
    "Pink",
    "Purple",
    "Fuchsia",
    "Rose",
    "Lavender",
    "Sky",
    "Mint",
    "Lemon",
    "Sand",
    "Cocoa",
    "Cream",
]

marker_colors_for_counting = [
    "All",
    "Blue",
    "Cyan",
    "Green",
    "Yellow",
    "Red",
    "Pink",
    "Purple",
    "Fuchsia",
    "Rose",
    "Lavender",
    "Sky",
    "Mint",
    "Lemon",
    "Sand",
    "Cocoa",
    "Cream",
]


# General functions
def get_all_timeline():
    """
    Get all existing timelines. Return a list containing all the timeline
    object.
    """
    all_timeline = []
    for timeline_index in range(1, project.GetTimelineCount() + 1, 1):
        all_timeline.append(project.GetTimelineByIndex(timeline_index))
    return all_timeline


def get_timeline_by_name(timeline_name: str):
    """Get timeline object by name."""
    all_timeline = get_all_timeline()
    timeline_dict = {timeline.GetName(): timeline for timeline in all_timeline}
    return timeline_dict.get(timeline_name)


def read_all_marker():
    markers = current_timeline.GetMarkers()
    return markers


def load_start_and_end_frames():
    """
    Load start and end frame into copy marker from area's timecode range
    """
    start_frame = DfttTimecode(
        current_timeline.GetStartFrame(), "auto", 24, False, True
    )
    end_frame = DfttTimecode(
        current_timeline.GetEndFrame(), "auto", 24, False, True
    )
    start_frame_tc = start_frame.timecode_output("smpte")
    end_frame_tc = end_frame.timecode_output("smpte")
    itm[start_timecode_id].PlaceholderText = start_frame_tc
    itm[end_timecode_id].PlaceholderText = end_frame_tc


def marker_number_display_message(
    marker_number: int, count_colored_marker: str = "All"
):
    """
    Accept a marker number parameter, and a parameter whether to count marker by
    color, add the appropriate message to the pathTree, and display the message
    to the user.
    """
    if count_colored_marker == "All":
        row = itm[messageTreeID].NewItem()
        if marker_number == 0:
            row.Text[0] = "There is no marker in this timeline."
        elif marker_number == 1:
            row.Text[0] = f"There is {marker_number} marker in this timeline."
        else:
            row.Text[0] = f"There are {marker_number} markers in this timeline."
        itm[messageTreeID].AddTopLevelItem(row)
    elif count_colored_marker in marker_colors:
        row = itm[messageTreeID].NewItem()
        if marker_number == 0:
            row.Text[0] = "There is no marker in this timeline."
        elif marker_number == 1:
            row.Text[0] = (
                f"There is {marker_number} {count_colored_marker} marker in "
                f"this timeline."
            )
        else:
            row.Text[0] = (
                f"There are {marker_number} {count_colored_marker} markers in "
                f"this timeline."
            )
        itm[messageTreeID].AddTopLevelItem(row)


start_up_markers = read_all_marker()

# Get items of the UI
itm = win.GetItems()
itm[markerColorForRemovalID].AddItems(marker_colors)
itm[markerColorForCountingID].AddItems(marker_colors_for_counting)

# Load all timelines into ComboBox
all_timelines: list[str] = [
    timeline.GetName() for timeline in get_all_timeline()
]
itm[timelinesID].AddItems(all_timelines)


# Events handlers
def on_close(ev):
    """Close the window."""
    dispatcher.ExitLoop()


def on_click_marker_counter(ev):
    itm[markerCountDisplayID].Clear()
    current_timeline = project.GetCurrentTimeline()

    if itm[markerColorForCountingID].CurrentText == "All":
        marker_number = len(current_timeline.GetMarkers())
        marker_number_display_message(marker_number)
        itm[markerCountDisplayID].Insert(str(marker_number))
    else:
        marker_about_to_count: str = itm[markerColorForCountingID].CurrentText
        marker_number = 0
        for marker_properties in current_timeline.GetMarkers().values():
            if marker_properties["color"] == marker_about_to_count:
                marker_number += 1
        marker_number_display_message(
            marker_number, count_colored_marker=marker_about_to_count
        )
        itm[markerCountDisplayID].Insert(str(marker_number))


def on_click_output_browse_button(ev):
    selected = fusion.RequestDir()
    if selected is None:
        itm[outputPathID].Text = ""
    else:
        itm[outputPathID].Text = str(selected)[:-1]
    return selected


def on_click_delete_marker_by_color_button(ev):
    current_timeline = project.GetCurrentTimeline()
    markers_about_to_delete = itm[markerColorForRemovalID].CurrentText
    if not bool(current_timeline.GetMarkers()):
        row = itm[messageTreeID].NewItem()
        row.Text[0] = "There is no marker to delete!"
        itm[messageTreeID].AddTopLevelItem(row)
    else:
        current_timeline.DeleteMarkersByColor(markers_about_to_delete)


def on_click_copy_markers_from_specified_timeline(ev):
    current_timeline = project.GetCurrentTimeline()
    markers_copy_target = get_timeline_by_name(itm[timelinesID].CurrentText)
    target_timeline_markers = markers_copy_target.GetMarkers()

    if (
        bool(itm[start_timecode_id].Text) is True
        and bool(itm[end_timecode_id].Text) is False
    ):
        start_timecode = DfttTimecode(
            itm[start_timecode_id].Text, "auto", 24, False, True
        )
        end_timecode = DfttTimecode(
            current_timeline.GetEndFrame(), "auto", 24, False, True
        )
    elif (
        bool(itm[start_timecode_id].Text) is False
        and bool(itm[end_timecode_id].Text) is True
    ):
        start_timecode = DfttTimecode("01:00:00:00", "auto", 24, False, True)
        end_timecode = DfttTimecode(
            itm[end_timecode_id].Text, "auto", 24, False, True
        )
    elif bool(itm[start_timecode_id].Text) and bool(itm[end_timecode_id].Text):
        start_timecode = DfttTimecode(
            itm[start_timecode_id].Text, "auto", 24, False, True
        )
        end_timecode = DfttTimecode(
            itm[end_timecode_id].Text, "auto", 24, False, True
        )
    else:
        start_timecode = DfttTimecode("01:00:00:00", "auto", 24, False, True)
        end_timecode = DfttTimecode(
            current_timeline.GetEndFrame(), "auto", 24, False, True
        )

    print(f"Start timecode: {start_timecode}")
    print(f"End timecode: {end_timecode}")

    # 把目标时间线上小于用户给定的 start timecode 或大于用户给定的 end timecode 的 markers 从
    # target_timeline_markers 这个 dict 里面删掉。
    for frame_id in list(target_timeline_markers):
        if (
            int(frame_id) + 86400 < start_timecode
            or int(frame_id) + 86400 > end_timecode
        ):
            target_timeline_markers.pop(frame_id)

    # 获取当前时间线下所有的 markers。
    current_timeline_markers = current_timeline.GetMarkers()
    # 如果当前时间线上在用户给定的 in and out timecode range 内有 marker 的话，那么先把这个范围的
    # marker 删掉。如果没有，则不执行 DeleteMarkerAtFrame()。
    for frame_id in current_timeline_markers:
        if start_timecode < int(frame_id) + 86400 < end_timecode:
            current_timeline.DeleteMarkerAtFrame(frame_id)

    # 最后把目标时间线上我们需要的 markers 添加到当前时间线已经被清理过（删除已经存在的 markers）的范围上。
    for frame_id in target_timeline_markers:
        current_timeline.AddMarker(
            frame_id,
            target_timeline_markers[frame_id]["color"],
            target_timeline_markers[frame_id]["name"],
            target_timeline_markers[frame_id]["note"],
            target_timeline_markers[frame_id]["duration"],
            target_timeline_markers[frame_id]["customData"],
        )


def on_click_undo_copy_and_paste_markers_button(ev):
    current_timeline = project.GetCurrentTimeline()
    all_markers = current_timeline.GetMarkers()
    for frameID in all_markers:
        current_timeline.DeleteMarkerAtFrame(frameID)

    for mk_frameId in start_up_markers:
        mk = start_up_markers[mk_frameId]
        color = str(mk["color"])
        duration = int(mk["duration"])
        note = str(mk["note"])
        name = str(mk["name"])
        custom_data = mk["customData"]
        o = current_timeline.AddMarker(
            mk_frameId, color, name, note, duration, custom_data
        )
        print(o)


def on_click_clear_messages_button(ev):
    itm[messageTreeID].Clear()


def on_click_update_start_and_end_frame_button(ev):
    load_start_and_end_frames()


# Assign events handlers
win.On.myWindow.Close = on_close
win.On[countMarkerID].Clicked = on_click_marker_counter
win.On[browseOutputFileManagerID].Clicked = on_click_output_browse_button
win.On[deleteMarkersByColorID].Clicked = on_click_delete_marker_by_color_button
win.On[
    copyMarkersFromSpecifiedTimelineID
].Clicked = on_click_copy_markers_from_specified_timeline
win.On[
    undoCopyAndPasteMarkersID
].Clicked = on_click_undo_copy_and_paste_markers_button
win.On[clearMessagesID].Clicked = on_click_clear_messages_button
win.On[
    update_start_and_end_frame_id
].Clicked = on_click_update_start_and_end_frame_button

if __name__ == "__main__":
    win.Show()
    load_start_and_end_frames()
    dispatcher.RunLoop()