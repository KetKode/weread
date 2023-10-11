from boringavatars import avatar

def generate_avatar(name, size=250, variant="beam", colors=None, title=False, square=False):
    if colors is None:
        colors = ["92A1C6", "146A7C", "F0AB3D", "C271B4", "C20D90"]

    avatar_svg = avatar(name, variant=variant, colors=colors, title=title, size=size, square=square)

    return avatar_svg
