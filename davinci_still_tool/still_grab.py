from resolve_init import GetResolve
import logging

# Constants
ALL_MARKERS = {}

# Set up logger
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter(
    "%(name)s %(levelname)s %(asctime)s at %(lineno)s: %(message)s",
    datefmt="%H:%M:%S",
)

# Add formatter to ch
ch.setFormatter(formatter)

# Add ch to logger
log.addHandler(ch)

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
timelineID = "Timelines in the mediapool"
copyCurrentTimelineMarkersID = "Copy current timeline markers"
pasteTimelineMarkersID = "Paste the markers just copied"

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
                            "ID": copyCurrentTimelineMarkersID,
                            "Text": "Copy Markers",
                            "Weight": 0,
                        }
                    ),
                    ui.Button(
                        {
                            "ID": pasteTimelineMarkersID,
                            "Text": "Paste Markers",
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

# Get items of the UI
itm = win.GetItems()
itm[markerColorID].AddItems(marker_colors)


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


def get_timeline_by_name(self, timeline_name: str):
    """Get timeline object by name."""
    all_timeline = self.get_all_timeline()
    timeline_dict = {timeline.GetName(): timeline for timeline in all_timeline}
    return timeline_dict.get(timeline_name)


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
    itm[pathTreeID].AddTopLevelItem(row)


def on_click_output_browse_button(ev):
    selected = fusion.RequestDir()
    itm[outputPathID].Text = str(selected)[:-1]
    return selected


def on_click_delete_marker_by_color_button(ev):
    current_timeline = project.GetCurrentTimeline()
    markers_about_to_delete = itm[markerColorID].CurrentText
    current_timeline.DeleteMarkersByColor(markers_about_to_delete)


def on_click_copy_current_timeline_markers(ev):
    current_timeline = project.GetCurrentTimeline()
    ALL_MARKERS = current_timeline.GetMarkers()
    row = itm[pathTreeID].NewItem()
    row.Text[
        0
    ] = f"Copied current timeline {current_timeline.GetName()} markers!"
    itm[pathTreeID].AddTopLevelItem(row)


def on_click_paste_timeline_markers(ev):
    current_timeline = project.GetCurrentTimeline()
    for color in marker_colors:
        current_timeline.DeleteMarkersByColor(color)
    for key in ALL_MARKERS:
        current_timeline.AddMarker(
            key,
            ALL_MARKERS[key]["color"],
            ALL_MARKERS[key]["name"],
            ALL_MARKERS[key]["note"],
            ALL_MARKERS[key]["duration"],
            ALL_MARKERS[key]["customData"],
        )


# Assign events handlers
win.On.myWindow.Close = on_close
win.On[countMarkerID].Clicked = on_click_marker_counter
win.On[browseOutputFileManagerID].Clicked = on_click_output_browse_button
win.On[deleteMarkersByColorID].Clicked = on_click_delete_marker_by_color_button
win.On[
    copyCurrentTimelineMarkersID
].Clicked = on_click_copy_current_timeline_markers
win.On[pasteTimelineMarkersID].Clicked = on_click_paste_timeline_markers

if __name__ == "__main__":
    win.Show()
    dispatcher.RunLoop()
