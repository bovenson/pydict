def get_screen_size(window):
    return (window.winfo_screenwidth(), window.winfo_screenheight())
def get_window_size(window):
    return (window.winfo_reqwidth(), window.winfo_reqheight())
def center_window(root, width, height):
    (screenwidth, screenheight) = get_screen_size(root)
    size = '%dx%d+%d+%d' % (width, height, int((screenwidth-width)/2), int((screenheight-height)/2))
    print('center window:', size)
    root.geometry(size)
