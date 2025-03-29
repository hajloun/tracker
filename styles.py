import dearpygui.dearpygui as dpg
def configure_styles():
    """Configure global theme and styles"""
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            # Text styling
            dpg.add_theme_color(dpg.mvThemeCol_Text, (230, 230, 230))

            # Window and background colors
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0))

            # Button styles
            dpg.add_theme_color(dpg.mvThemeCol_Button, (70, 70, 70))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (90, 90, 90))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 100, 100))

            # Input text styles
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (60, 60, 60))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (70, 70, 70))

            # Padding and spacing
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5,)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 0,)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 5)

    return global_theme