local boolRefresh = false
local ui = fu.UIManager
local disp = bmd.UIDispatcher(ui)
local width, height = 270, 280
local IDButton = 0

win = disp:AddWindow({
    ID = 'MyWin',
    TargetID = 'MyWin',
    WindowTitle = 'Resolve PolyClipEdit',
    Geometry = {200, 250, width, height},

    Spacing = 0,

    ui:VGroup{
        ID = 'root',
        ui:VGroup{
            Weight = 0,
            ID = "GQuick",
            ui:HGroup{ui:Label{
                Weight = 1,
                Text = "Track No"
            }, ui:ComboBox{
                Weight = 1,
                ID = "qTrack",
                CurrentText = "TimeLine",
                Editable = 'true',
                Events = {
                    TextChanged = true
                }
            }},
            ui:HGroup{ui:Label{
                Weight = 1,
                Text = "Marker Color"
            }, ui:ComboBox{
                Weight = 1,
                ID = "qMarkerColor",
                CurrentText = "TimeLine",
                Editable = 'true',
                Events = {
                    TextChanged = true
                }
            }},
            ui:HGroup{ui:Label{
                Weight = 1,
                Text = "Clip Color"
            }, ui:ComboBox{
                Weight = 1,
                ID = "qClipColor",
                CurrentText = "TimeLine",
                Editable = 'true',
                Events = {
                    TextChanged = true
                }
            }},
            ui:HGroup{ui:Label{
                Weight = 1,
                ID = "Gap",
                Text = "Gap"
            }, ui:LineEdit{
                Weight = 1,
                ID = "qGap",
                Text = "100",
                Editable = 'true'
            }},
            ui:HGroup{ui:Button{
                Weight = 1,
                ID = "bOffsetLeft",
                Text = "Offset"
            }, ui:LineEdit{
                Weight = 1,
                ID = "qOffsetLeft",
                Text = "0",
                Editable = 'true'
            }},
            ui:HGroup{ui:Button{
                Weight = 1,
                ID = "bDuration",
                Text = "Duration"
            }, ui:LineEdit{
                Weight = 1,
                ID = "qDuration",
                Text = "1",
                Editable = 'true'
            }},
            ui:VGap(8),
            ui:HGroup{ui:Button{
                Weight = 1,
                ID = "qAppendMarkers",
                Text = "Append to Timeline"
            }},
            ui:HGroup{ui:Button{
                Weight = 1,
                ID = "qRenderMarkers",
                Text = "Add to Render Queue"
            }},
            ui:VGap(8),
            ui:HGroup{ui:Label{
                Weight = 1,
                ID = "BPMEdit",
                Text = "BPM Edit"
            }, ui:LineEdit{
                Weight = 1,
                ID = "qBPMEdit",
                Text = "0",
                Editable = 'true'
            }}
        }

    }
})

itm = win:GetItems()
notify = ui:AddNotify('Comp_Activate_Tool')

local combobox = win:GetItems().qTrack
combobox:AddItem('All')
combobox:AddItem('TL (Render only)')
combobox:AddItem('1')
combobox:AddItem('2')
combobox:AddItem('3')
combobox:AddItem('4')
combobox:AddItem('5')
combobox:AddItem('6')
combobox:AddItem('7')
combobox:AddItem('8')
combobox:AddItem('9')
combobox:AddItem('10')

local combobox = win:GetItems().qMarkerColor
combobox:AddItem('All')
combobox:AddItem('Blue')
combobox:AddItem('Cyan')
combobox:AddItem('Green')
combobox:AddItem('Yellow')
combobox:AddItem('Red')
combobox:AddItem('Pink')
combobox:AddItem('Purple')
combobox:AddItem('Fuchsia')
combobox:AddItem('Rose')
combobox:AddItem('Lavender')
combobox:AddItem('Sky')
combobox:AddItem('Mint')
combobox:AddItem('Lemon')
combobox:AddItem('Sand')
combobox:AddItem('Cocoa')
combobox:AddItem('Cream')

local combobox = win:GetItems().qClipColor
combobox:AddItem('All')
combobox:AddItem('Orange')
combobox:AddItem('Apricot')
combobox:AddItem('Yellow')
combobox:AddItem('Lime')
combobox:AddItem('Olive')
combobox:AddItem('Green')
combobox:AddItem('Teal')
combobox:AddItem('Navy')
combobox:AddItem('Blue')
combobox:AddItem('Purple')
combobox:AddItem('Violet')
combobox:AddItem('Pink')
combobox:AddItem('Tan')
combobox:AddItem('Beige')
combobox:AddItem('Brown')
combobox:AddItem('Chocolate')

function round(num, numDecimalPlaces)
    local mult = 10 ^ (numDecimalPlaces or 0)
    return math.floor(num * mult + 0.5) / mult
end

function fract(x)
    return x - math.floor(x)
end

function win.On.bOffsetLeft.Clicked(ev)
    frames = GetFramesFromBPM()
    if frames ~= "inf" then
        itm.qOffsetLeft.Text = frames
    end

end

function win.On.bDuration.Clicked(ev)
    frames = GetFramesFromBPM()
    if frames ~= "inf" then
        itm.qDuration.Text = frames
    end

end

function BPMCalc(BPM)
    b2 = 1
    b3 = 0
    _, _, b1, b2, b3 = string.find(BPM, "(.+)*(.+)+(.+)")
    if b1 == nil then
        _, _, b1, b2, b3 = string.find(BPM, "(.+)*(.+)-(.+)")
        if b3 ~= nil then
            b3 = -b3
        end
    end
    if b1 == nil then
        _, _, b1, b2, b3 = string.find(BPM, "(.+)/(.+)+(.+)")
        if b2 ~= nil then
            b2 = 1 / b2
        end
    end
    if b1 == nil then
        _, _, b1, b2, b3 = string.find(BPM, "(.+)/(.+)-(.+)")
        if b2 ~= nil then
            b2 = 1 / b2
        end
        if b3 ~= nil then
            b3 = -b3
        end
    end
    if b1 == nil then
        b3 = 0
        _, _, b1, b2 = string.find(BPM, "(.+)*(.+)")
    end
    if b1 == nil then
        b3 = 0
        _, _, b1, b2 = string.find(BPM, "(.+)/(.+)")
        if b2 ~= nil then
            b2 = 1 / b2
        end
    end
    if b1 == nil then
        b2 = 1
        b3 = 0
        _, _, b1 = string.find(BPM, "(.+)")
    end
    BPM = b1 * b2 + b3
    return BPM
end

function GetFramesFromBPM()
    pm = resolve:GetProjectManager()
    proj = pm:GetCurrentProject()
    tl = pm:GetCurrentProject():GetCurrentTimeline()
    fps = tl:GetSetting('timelineFrameRate')
    bpm = BPMCalc(tostring(itm.qBPMEdit.Text))
    return tostring(round(fps * 60 / bpm, 5))
end

function BMDLength(tlLen)
    pm = resolve:GetProjectManager()
    proj = pm:GetCurrentProject()
    tl = pm:GetCurrentProject():GetCurrentTimeline()
    fps = tl:GetSetting('timelineFrameRate')
    secSum = math.floor(tlLen / fps)
    hh, mm, ss, fr = "00"

    hours = math.floor(secSum / (60 * 60))
    if hours < 10 then
        hh = "0" .. hours
    else
        hh = hours
    end
    if hours == 0 then
        hh = "00"
    end
    minutes = math.floor(secSum / 60) - (hours * 60)
    if minutes < 10 then
        mm = "0" .. minutes
    else
        mm = minutes
    end
    if minutes == 0 then
        mm = "00"
    end
    seconds = math.floor(tlLen / fps) - (hours * 60 * 60) - (minutes * 60)
    if seconds < 10 then
        ss = "0" .. seconds
    else
        ss = seconds
    end
    if seconds == 0 then
        ss = "00"
    end
    frames = round(((tlLen / fps) - math.floor(tlLen / fps)) * fps, 0)
    if frames < 10 then
        fr = "0" .. frames
    else
        fr = frames
    end
    if frames == 0 then
        fr = "00"
    end
    return (hh .. ":" .. mm .. ":" .. ss .. ":" .. fr)
end

function BMDTimeFrames(tm)
    pm = resolve:GetProjectManager()
    proj = pm:GetCurrentProject()
    tl = pm:GetCurrentProject():GetCurrentTimeline()
    fps = tl:GetSetting('timelineFrameRate')
    sign = 1
    if string.find(tm, "-") ~= nil then
        sign = -1
    end
    _, _, hr, mi, se, fr = string.find(tm, "(%d+):(%d+):(%d+):(%d+)")
    if hr == nil then
        hr = 0
        _, _, mi, se, fr = string.find(tm, "(%d+):(%d+):(%d+)")
    end
    if mi == nil then
        mi = 0
        _, _, se, fr = string.find(tm, "(%d+):(%d+)")
    end
    if se == nil then
        se = 0
        _, _, fr = string.find(tm, "(%d+)")
    end
    if fr == nil then
        fr = 0
    end
    frames = (hr * 60 * 60 + mi * 60 + se) * fps + fr
    return frames * sign
end

function disp.On.Comp_Activate_Tool(ev)

end

function win.On.MyWin.Close(ev)
    disp:ExitLoop()
end

function getFolder(parentFolder, childFolder, mp)
    for folder in pairs(parentFolder:GetSubFolderList()) do
        if folder:GetName() == childFolder then
            return folder
        else
            return mp:AddSubFolder(parentFolder, childFolder)
        end
    end
end

stopFlag = 0
function searchForRootFolder(mp, timelineItemName)
    local clipItem
    rootfolder = mp:GetRootFolder()
    rootfolderName = rootfolder:GetName()
    clipItems = rootfolder:GetClips()
    for clipIndex, key in ipairs(clipItems) do
        clipName = clipItems[clipIndex]:GetClipProperty('Clip Name')
        -- print(rootfolderName.."/"..clipName)
        if clipName == timelineItemName then
            stopFlag = 1
            clipItem = clipItems[clipIndex]
            print(clipItems)
            return rootfolderName, clipItems, clipIndex
        end
    end
    return rootfolderName, nil, 0
end

function searchForSubFolder(folderN, mediafolder, timelineItemName)
    local clipItem
    mediafolderName = mediafolder:GetName()
    subfolders = mediafolder:GetSubFolderList()
    for i, subfolder in pairs(subfolders) do
        if i ~= "__flags" then
            subfolderName = subfolder:GetName()
            clipItems = subfolder:GetClips()
            for clipIndex, key in ipairs(clipItems) do
                clipName = clipItems[clipIndex]:GetClipProperty('Clip Name')
                -- print(folderN.."/"..subfolderName.."/"..clipName)
                if clipName == timelineItemName then
                    stopFlag = 1
                    clipItem = clipItems[clipIndex]
                    print(clipItems)
                    return subfolders, clipItems, clipIndex
                end
            end
        end
    end
    return subfolders, nil, 0
end

function RunClips(timelineItemName)
    stopFlag = 0
    pm = resolve:GetProjectManager()
    proj = pm:GetCurrentProject()
    mp = proj:GetMediaPool()
    preFolderName, clipItems, clipIndex = searchForRootFolder(mp, timelineItemName)
    if stopFlag == 1 then
        return clipItems, clipIndex
    end
    subfolders, clipItems, clipIndex = searchForSubFolder(preFolderName, mp:GetRootFolder(), timelineItemName)
    if stopFlag == 1 then
        return clipItems, clipIndex
    end
    folder = tostring(mp:GetRootFolder():GetName())
    folder1 = ""
    folder2 = ""
    folder3 = ""
    folder4 = ""
    folder1old = ""
    folder2old = ""
    folder3old = ""
    folder4old = ""
    for i, subfolder in pairs(subfolders) do
        if i ~= "__flags" then
            subfolders1, clipItems, clipIndex = searchForSubFolder(folder .. "/" .. subfolder:GetName(), subfolder,
                timelineItemName)
            if stopFlag == 1 then
                return clipItems, clipIndex
            end
            folder1 = subfolder:GetName()
            if folder1 == nil then
                folder1 = folder1old
            else
                folder1old = folder1
            end
            folder2old = ""
            for i1, subfolder1 in pairs(subfolders1) do
                if i1 ~= "__flags" then
                    subfolders2, clipItems, clipIndex = searchForSubFolder(
                        folder .. "/" .. folder1 .. "/" .. subfolder1:GetName(), subfolder1, timelineItemName)
                    if stopFlag == 1 then
                        return clipItems, clipIndex
                    end
                    folder2 = subfolder1:GetName()
                    if folder2 == nil then
                        folder2 = folder2old
                    else
                        folder2old = folder2
                    end
                    folder3old = ""
                    for i2, subfolder2 in pairs(subfolders2) do
                        if i2 ~= "__flags" then
                            subfolders3, clipItems, clipIndex = searchForSubFolder(
                                folder .. "/" .. folder1 .. "/" .. folder2 .. "/" .. subfolder2:GetName(), subfolder2,
                                timelineItemName)
                            if stopFlag == 1 then
                                return clipItems, clipIndex
                            end
                            folder3 = subfolder2:GetName()
                            if folder3 == nil then
                                folder3 = folder3old
                            else
                                folder3old = folder3
                            end
                            folder4old = ""
                            for i3, subfolder3 in pairs(subfolders3) do
                                if i3 ~= "__flags" then
                                    subfolders4, clipItems, clipIndex =
                                        searchForSubFolder(folder .. "/" .. folder1 .. "/" .. folder2 .. "/" .. folder3 ..
                                                               "/" .. subfolder3:GetName(), subfolder3, timelineItemName)
                                    if stopFlag == 1 then
                                        return clipItems, clipIndex
                                    end
                                    folder4 = subfolder3:GetName()
                                    if folder4 == nil then
                                        folder4 = folderold
                                    else
                                        folder4old = folder4
                                    end
                                    folder4old = ""
                                    for i4, subfolder4 in pairs(subfolders4) do
                                        if i4 ~= "__flags" then
                                            subfolders5, clipItems, clipIndex =
                                                searchForSubFolder(folder .. "/" .. folder1 .. "/" .. folder2 .. "/" ..
                                                                       folder3 .. "/" .. folder4 .. "/" ..
                                                                       subfolder4:GetName(), subfolder4,
                                                    timelineItemName)
                                            if stopFlag == 1 then
                                                return clipItems, clipIndex
                                            end
                                            folder5 = subfolder4:GetName()
                                            if folder5 == nil then
                                                folder45 = folderold
                                            else
                                                folder5old = folder5
                                            end
                                        end
                                    end

                                end
                            end
                        end
                    end
                end
            end
        end
    end
    return clipItems, clipIndex
end

function RunMarkers(boolRender)
    track = tostring(itm.qTrack.CurrentText)
    colorMarker = tostring(itm.qMarkerColor.CurrentText)
    colorClip = tostring(itm.qClipColor.CurrentText)
    gap = tonumber(tostring(itm.qGap.Text))
    offset = tonumber(tostring(itm.qOffsetLeft.Text))
    duration = tonumber(tostring(itm.qDuration.Text))
    local format = "tif"
    local codec = "RGB16LZW"
    resolve = Resolve()
    projectManager = resolve:GetProjectManager()
    project = projectManager:GetCurrentProject()
    mediapool = project:GetMediaPool()
    timeline = project:GetCurrentTimeline()
    timelineName = timeline:GetName()
    timelineFPS = timeline:GetSetting('timelineFrameRate')
    timelineVideoTrackCount = timeline:GetTrackCount("video")
    timelineDuration = (timeline:GetEndFrame() - timeline:GetStartFrame())
    timelineStartFrame = timeline:GetStartFrame()
    trackNum = 0
    trackFact = 0
    if track == "All" then
        trackNum = 1
        frackFact = 0
    else
        trackNum = tonumber(track)
        trackFact = 1
    end
    renderSettingsArr = {}
    clipArr = {}

    markers = timeline:GetMarkers()

    if track == "All" or track == "TL (Render only)" then
        for markerStartFrame in pairs(markers) do
            markerName = markers[markerStartFrame]['name']
            markerColor = markers[markerStartFrame]['color']
            markerDuration = markers[markerStartFrame]['duration']
            timelinePosition = timelineStartFrame + markerStartFrame
            if colorMarker == markerColor or colorMarker == "All" then
                SubClip = {}
                renderSettings = {}
                if boolRender == 1 then
                    renderSettings["MarkIn"] = timelinePosition + offset
                    renderSettings["MarkOut"] = timelinePosition + markerDuration + duration + offset - 2
                    renderSettings["CustomName"] = (timelineName .. "_" .. markerStartFrame):gsub("[./\\?%%*:|\"<>&#]",
                        "_")
                    table.insert(renderSettingsArr, renderSettings)
                end
            end
        end
    end

    if track ~= "TL (Render only)" then
        for index = trackNum, trackNum * (1 - trackFact) + timelineVideoTrackCount * trackFact, 1 do
            timelineItems = timeline:GetItemsInTrack("video", index)
            for timelineItem in pairs(timelineItems) do
                timelineItemName = timelineItems[timelineItem]:GetName()
                timelineItemStartFrame = timelineItems[timelineItem]:GetStart()
                timelineItemLeftOffset = timelineItems[timelineItem]:GetLeftOffset()
                timelineItemColor = timelineItems[timelineItem]:GetClipColor()
                markers = timelineItems[timelineItem]:GetMarkers()
                for markerStartFrame in pairs(markers) do
                    markerName = markers[markerStartFrame]['name']
                    markerColor = markers[markerStartFrame]['color']
                    markerDuration = markers[markerStartFrame]['duration']
                    timelinePosition = timelineItemStartFrame - timelineItemLeftOffset + markerStartFrame
                    if colorMarker == markerColor or colorMarker == "All" then
                        if colorClip == timelineItemColor or colorClip == "All" then
                            SubClip = {}
                            renderSettings = {}
                            if boolRender == 1 then
                                renderSettings["MarkIn"] = timelinePosition + offset
                                renderSettings["MarkOut"] = timelinePosition + markerDuration + duration + offset - 2
                                renderSettings["CustomName"] =
                                    (timelineItemName .. "_" .. markerStartFrame):gsub("[./\\?%%*:|\"<>&#]", "_")
                                table.insert(renderSettingsArr, renderSettings)
                            else
                                clipItms, clipIndx = RunClips(timelineItemName)
                                clipItm = clipItms[clipIndx]
                                clipFPS = clipItm:GetClipProperty('FPS')

                                SubClip["mediaPoolItem"] = clipItm
                                SubClip["startFrame"] = ((markerStartFrame + offset) * clipFPS / timelineFPS)
                                SubClip["endFrame"] = ((markerStartFrame + markerDuration + duration + offset - 2) *
                                                          clipFPS / timelineFPS)
                                SubClip["Position"] = timelinePosition
                                -- print(timelineItemColor.." "..timelineName.." "..timelineItemName.." "..timelinePositionTimeCode.." "..markerStartFrame.."  "..markerName.." "..markerColor.." "..markerDuration)
                                table.insert(clipArr, SubClip)
                            end
                        end
                    end
                end

            end
        end
    end
    n = 0
    if boolRender == 1 then
        table.sort(renderSettingsArr, function(k1, k2)
            return k1.MarkIn < k2.MarkIn
        end)
        project:DeleteAllRenderJobs()
        -- project:SetCurrentRenderMode(1) -- single Clips
        -- project:SetCurrentRenderFormatAndCodec(format, codec)
        for i, renderSettings in ipairs(renderSettingsArr) do
            renderSettings.CustomName = string.sub(tostring(i + 1000), 2, 4) .. "_" .. renderSettings.CustomName
            project:SetRenderSettings(renderSettings)
            project:AddRenderJob()
        end
    else
        table.sort(clipArr, function(k1, k2)
            return k1.Position < k2.Position
        end)
        for i, SubClip in ipairs(clipArr) do
            n = n + 1
            if n == 1 then
                SubClip["recordFrame"] = timeline:GetEndFrame() + gap
            end
            itemFrac = (mediapool:AppendToTimeline({SubClip}))
            -- print(SubClip.Position.."  "..SubClip.startFrame.."  "..SubClip.endFrame) 
        end
    end

end

function win.On.qAppendMarkers.Clicked(ev)
    stopFlag = 0
    RunMarkers(0)
end

function win.On.qRenderMarkers.Clicked(ev)
    stopFlag = 0
    print("Render")
    RunMarkers(1)
end

local function IsEmpty(arg)
    return arg == nil or arg == ''
end

local function Export(timeline, filePath, exportType, exportSubType)
    local result = false
    if IsEmpty(exportSubType) then
        result = timeline:Export(filePath, exportType)
    else
        result = timeline:Export(filePath, exportType, exportSubType)
    end

    if result then
        print("Timeline exported to " .. filePath .. " successfully.")
    else
        print("Timeline export failed.")
    end
    Export(timeline, csvFilePath, resolve.EXPORT_TEXT_CSV)
end

function FileNameExt(filename)
    homeDir = os.getenv("HOME")
    return homeDir .. "/" .. filename
end

function MovePlayhead(Forward, Fast)
    res, offset, framesD = 0

    pm = resolve:GetProjectManager()
    tl = pm:GetCurrentProject():GetCurrentTimeline()
    ctc = (tl:GetCurrentTimecode())
    Data = tl:GetMarkerCustomData(0)
    _, _, track, clip, framesD, res, offset, length = string.find(Data, "(.+);(.+);(.+);(.+);(.+);(.+)")

    if Fast == 1 then
        framesD = framesD * res
    end
    frames = BMDTimeFrames(ctc)
    frames = frames + framesD * Forward

    if Forward == 1 then
        frames = math.floor((frames + 0.5) / framesD) * framesD + fract(offset / framesD) * framesD
    else
        frames = math.ceil((frames - 0.5 - fract(offset / framesD) * framesD) / framesD) * framesD +
                     fract(offset / framesD) * framesD
    end

    ctc2 = BMDLength(frames)
    tl:SetCurrentTimecode(ctc2)
end

app:AddConfig('MyWin', {Target {
    ID = 'MyWin'
}, Hotkeys {
    Target = 'MyWin',
    Defaults = true,

    CONTROL_W = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}',
    CONTROL_F4 = 'Execute{cmd = [[app.UIManager:QueueEvent(obj, "Close", {})]]}'
}})

win:Show()

disp:RunLoop()
win:Hide()

app:RemoveConfig('MyWin')
collectgarbage()
