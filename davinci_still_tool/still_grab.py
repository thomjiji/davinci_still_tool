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
outputPathID = "Output Path"
testClickID = "Test Click"
pathTreeID = "Path Tree"
countMarkerID = "Count Marker"
browseOutputFileManagerID = "Browse File Manager"
markerColorForRemovalID = "Marker color for removal"
markerColorForCountingID = "Marker color for counting"
deleteMarkersByColorID = "Delete Marker By Color"
timelinesID = "Timelines in the mediapool"
copyMarkersFromSpecifiedTimelineID = "Copy markers from specified timeline"
markerCountDisplayID = "Display marker counts"
undoCopyAndPasteMarkersID = "Undo copy and paste markers"

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

copy_markers_from_area = ui.HGroup(
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
)

copy_and_paste_button_and_undo = ui.HGroup(
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
    ],
)


# Compose the whole UI
win = dispatcher.AddWindow(
    {
        "ID": "myWindow",
        "Geometry": [
            750,
            200,
            350,
            400,
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
            copy_and_paste_button_and_undo,
            #
            ui.Label(
                {
                    "StyleSheet": "max-height: 1px; background-color: rgb(10,10,10)",
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
                ],
            ),
            ui.Tree(
                {
                    "ID": pathTreeID,
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


def marker_number_display_message(
    marker_number: int, count_colored_marker: str = "All"
):
    """
    Accept a marker number parameter, and a parameter whether to count marker by
    color, add the appropriate message to the pathTree, and display the message
    to the user.
    """
    if count_colored_marker == "All":
        row = itm[pathTreeID].NewItem()
        if marker_number == 0:
            row.Text[0] = f"There is no marker in this timeline."
        elif marker_number == 1:
            row.Text[0] = f"There is {marker_number} marker in this timeline."
        else:
            row.Text[0] = f"There are {marker_number} markers in this timeline."
        itm[pathTreeID].AddTopLevelItem(row)
    elif count_colored_marker in marker_colors:
        row = itm[pathTreeID].NewItem()
        if marker_number == 0:
            row.Text[0] = f"There is no marker in this timeline."
        elif marker_number == 1:
            row.Text[
                0
            ] = f"There is {marker_number} {count_colored_marker} marker in this timeline."
        else:
            row.Text[
                0
            ] = f"There are {marker_number} {count_colored_marker} markers in this timeline."
        itm[pathTreeID].AddTopLevelItem(row)


start_up_markers = read_all_marker()

# Get items of the UI
itm = win.GetItems()
itm[markerColorForRemovalID].AddItems(marker_colors)
itm[markerColorForCountingID].AddItems(marker_colors_for_counting)

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
    if selected == None:
        itm[outputPathID].Text = ""
    else:
        itm[outputPathID].Text = str(selected)[:-1]
    return selected


def on_click_delete_marker_by_color_button(ev):
    current_timeline = project.GetCurrentTimeline()
    markers_about_to_delete = itm[markerColorForRemovalID].CurrentText
    if not bool(current_timeline.GetMarkers()):
        row = itm[pathTreeID].NewItem()
        row.Text[0] = f"There is no marker to delete!"
        itm[pathTreeID].AddTopLevelItem(row)
    else:
        current_timeline.DeleteMarkersByColor(markers_about_to_delete)


def on_click_copy_markers_from_specified_timeline(ev):
    current_timeline = project.GetCurrentTimeline()
    markers_copy_target = get_timeline_by_name(itm[timelinesID].CurrentText)
    all_markers = markers_copy_target.GetMarkers()  # type: ignore

    for color in marker_colors:
        # If there is no marker in the current timeline, then skip this for loop
        # and add marker directly.
        if not bool(current_timeline.GetMarkers()):
            break
        # If the current timeline has markers, use this for loop to delete
        # markers of all color in turn.
        else:
            current_timeline.DeleteMarkersByColor(color)
    for key in all_markers:
        current_timeline.AddMarker(
            key,
            all_markers[key]["color"],
            all_markers[key]["name"],
            all_markers[key]["note"],
            all_markers[key]["duration"],
            all_markers[key]["customData"],
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
        customData = mk["customData"]
        o = current_timeline.AddMarker(
            mk_frameId, color, name, note, duration, customData
        )
        print(o)


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

if __name__ == "__main__":
    win.Show()
    dispatcher.RunLoop()
