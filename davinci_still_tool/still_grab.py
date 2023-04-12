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
markerColorID = "Marker Color"
deleteMarkersByColorID = "Delete Marker By Color"
timelinesID = "Timelines in the mediapool"
copyMarkersFromSpecifiedTimelineID = "Copy markers from specified timeline"

win = dispatcher.AddWindow(
    {
        "ID": "myWindow",
        "Geometry": [
            500,
            300,
            800,
            600,
        ],
        "WindowTitle": "Grab Still",
    },
    ui.VGroup(
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
            ),
            ui.HGroup(
                {
                    "Spacing": 5,
                    "Weight": 0,
                },
                [
                    ui.ComboBox({"ID": markerColorID, "Weight": 0}),
                    ui.Button(
                        {
                            "ID": deleteMarkersByColorID,
                            "Text": "Delete Marker",
                            "Weight": 0,
                        }
                    ),
                    ui.Button(
                        {
                            "ID": countMarkerID,
                            "Text": "Count Marker",
                            "Weight": 0,
                        }
                    ),
                    ui.Button(
                        {
                            "ID": copyMarkersFromSpecifiedTimelineID,
                            "Text": "Copy Markers From",
                            "Weight": 0,
                        }
                    ),
                    ui.ComboBox(
                        {
                            "ID": timelinesID,
                            "Weight": 0,
                        }
                    ),
                ],
            ),
            ui.Tree(
                {
                    "ID": pathTreeID,
                    "AlternatingRowColors": True,
                    "HeaderHidden": True,
                    "SelectionMode": "ExtendedSelection",
                    "Weight": 1,
                    "AutoScroll": True,
                    "SortingEnabled": False,
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


# Get items of the UI
itm = win.GetItems()
itm[markerColorID].AddItems(marker_colors)

all_timelines: list[str] = [
    timeline.GetName() for timeline in get_all_timeline()
]
itm[timelinesID].AddItems(all_timelines)


# Events handlers
def on_close(ev):
    """Close the window."""
    dispatcher.ExitLoop()


def on_click_marker_counter(ev):
    current_timeline = project.GetCurrentTimeline()
    marker_number = len(current_timeline.GetMarkers())
    row = itm[pathTreeID].NewItem()
    if marker_number > 1:
        row.Text[
            0
        ] = f"There are {str(marker_number)} markers in this timeline."
    elif marker_number == 1:
        row.Text[0] = f"There is {str(marker_number)} marker in this timeline."
    else:
        row.Text[0] = f"There is no marker in this timeline."
    itm[pathTreeID].AddTopLevelItem(row)


def on_click_output_browse_button(ev):
    selected = fusion.RequestDir()
    itm[outputPathID].Text = str(selected)[:-1]
    return selected


def on_click_delete_marker_by_color_button(ev):
    current_timeline = project.GetCurrentTimeline()
    markers_about_to_delete = itm[markerColorID].CurrentText
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
        if not bool(current_timeline.GetMarkers()):
            break
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


# Assign events handlers
win.On.myWindow.Close = on_close
win.On[countMarkerID].Clicked = on_click_marker_counter
win.On[browseOutputFileManagerID].Clicked = on_click_output_browse_button
win.On[deleteMarkersByColorID].Clicked = on_click_delete_marker_by_color_button
win.On[
    copyMarkersFromSpecifiedTimelineID
].Clicked = on_click_copy_markers_from_specified_timeline

if __name__ == "__main__":
    win.Show()
    dispatcher.RunLoop()
