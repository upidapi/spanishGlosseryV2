def get_mods(event):
    s = event.state

    # Manual way to get the modifiers
    ctrl = (s & 0x4) != 0
    alt = (s & 0x8) != 0 or (s & 0x80) != 0
    shift = (s & 0x1) != 0

    mods = []
    if ctrl:
        mods.append('ctrl')
    if alt:
        mods.append('alt')
    if shift:
        mods.append('shift')

    return mods
