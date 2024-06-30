from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import subprocess

@hook.subscribe.startup
def run_every_startup():
    subprocess.Popen(['picom'])
    subprocess.Popen(['nitrogen', '--restore'])

mod = "mod4"
terminal = "alacritty"
browser = "firefox"
runner = "rofi"

colors = {
    "background": "#1d1f21",
    "foreground": "#c5c8c6", 
    "black":      '#282a2e',
    "red":        '#a54242',
    "green":      '#8c9440',
    "yellow":     '#de935f',
    "blue":       '#5f819d',
    "magenta":    '#85678f',
    "cyan":       '#5e8d87',
    "white":      '#707880',
    }

colorsbright = {
    "background": "#1d1f21",
    "foreground": "#c5c8c6",
    "black":      '#373b41',
    "red":        '#cc6666',
    "green":      '#b5bd68',
    "yellow":     '#f0c674',
    "blue":       '#81a2be',
    "magenta":    '#b294bb',
    "cyan":       '#8abeb7',
    "white":      '#c5c8c6',
    }

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "h", lazy.layout.swap_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.swap_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod], "i", lazy.layout.grow(), desc="Grow window"),
    Key([mod], "m", lazy.layout.shrink(), desc="Shrink window"),
    Key([mod], "n", lazy.layout.reset(), desc="Reset all window sizes"),
    Key([mod, 'shift'], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window",),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn(runner + ' -show combi -modes combi -combi-modes "window,drun,run"'), desc="Spawn rofi"),
    Key([mod], "b", lazy.spawn(browser), desc="Spawn Firefox"),
    Key([mod], "e", lazy.spawn(terminal + ' -e ranger'), desc="Spawn Ranger"),
]

for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": colors["white"],
    "border_normal": colors["black"],
}

layouts = [
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrains Mono",
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    filename = "/home/vic/Images/arch2.png",
                    scale = True
                    ),
                widget.Prompt(
                    fontsize = 14,
                    foreground = colors["foreground"],
                    #background = colors["background"]
                    ),
                widget.GroupBox(
                    fontsize = 16,
                    margin_x = 5,
                    margin_y = 5,
                    padding_x = 1,
                    padding_y = 0,
                    borderwidth = 3,
                    active = colors["red"],
                    inactive = colors["foreground"],
                    rounded = False,
                    highlight_method = "line",
                    this_current_screen_border = colors["red"],
                    this_screen_border = colors["white"],
                    other_current_screen_border = colors["red"],
                    other_screen_border = colors["white"],
                    #background = colors["background"]
                    ),
                widget.Sep(),
                widget.WindowName(
                    #background = colors["background"],
                    foreground = colors["foreground"],
                    max_chars = 40
                    ),
                #widget.CPU(),
                widget.CheckUpdates(),
                #widget.Net(),
                #widget.Wlan(),
                widget.Sep(),
                widget.Volume(),
                #widget.Backlight(),
                widget.Sep(),
                widget.BatteryIcon(
                    theme_path = "~/.config/qtile/assets/battery/",
                    scale = True,
                    #background = colors['magenta']
                    ),
                widget.Battery(
                    font = "JetBrains Mono Bold",
                    foreground = colors['red'],
                    format = '{percent:2.0%}'
                    ),
                widget.Sep(),
                widget.Clock(
                    foreground = colors['foreground'],
                    format="%d.%m.%Y %A %H:%M:%S",
                    #background= colors['background']
                    ),
            ],
            30,
            background = '000000.4',
        ),
    ),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"), 
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),  
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "LG3D"
