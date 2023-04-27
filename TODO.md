TODO:

- Marker Counter 必须要在有时间线开启的情况下才能正常加载 Line 459
- copy target timeline 的部分 marker 只 works 在两个 timeline 是同样长度的情况下，如果 target timeline 要 copy 的部分
  marker 的时间码超过了当前时间线的总长度，那么不 work
- abstract messages tree area into one block that can be reusable.
- Scene 的 sorted 的问题

DONE:

- Timeline creator append_to_timeline function bug: sorted() 函数的排序还是基于 str 的，因此 1, 10, 11, 2, 3, 4… 这样的问题
- Marker Counter message 显示时间线名称