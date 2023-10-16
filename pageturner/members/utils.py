from boringavatars import avatar

def generate_avatar(name, size=250, variant="beam", colors=None, title=False, square=False):
    if colors is None:
        colors = ["92A1C6", "146A7C", "F0AB3D", "C271B4", "C20D90", "1AC992", "F79216", "#D64922", "#5E2B46", "#F03C9B", "772CC7"]

    avatar_svg = avatar(name, variant=variant, colors=colors, title=title, size=size, square=square)

    return avatar_svg
