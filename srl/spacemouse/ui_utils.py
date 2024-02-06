# Copyright (c) 2022-2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the MIT License [see LICENSE for details].


import omni.ui as ui
from omni.kit.window.property.templates import LABEL_WIDTH, LABEL_HEIGHT
from omni.isaac.ui.ui_utils import add_separator, add_line_rect_flourish
from omni.isaac.ui.style import get_style, BUTTON_WIDTH, COLOR_X, COLOR_Y, COLOR_Z
from omni.kit.window.extensions import SimpleCheckBox
import numpy as np

""" Most of these are pulled from omni.isaac.ui.ui_utils but with the tooltip formatting removed
"""

def xyz_plot_builder(
    label="",
    data=[],
    min=-1,
    max=1,
    type=ui.Type.LINE,
    value_stride=1,
    value_names=("X", "Y", "Z"),
    tooltip="",
    include_norm=False
):
    """[summary]

    Args:
        label (str, optional):  Label to the left of the UI element. Defaults to "".
        default_val (bool, optional): Checkbox default. Defaults to False.
        on_clicked_fn (Callable, optional): Checkbox Callback function. Defaults to lambda x: None.
        data list(), optional): Data to plat. Defaults to None.
        min (int, optional): Min Y Value. Defaults to -1.
        max (int, optional): Max Y Value. Defaults to 1.
        type (ui.Type, optional): Plot Type. Defaults to ui.Type.LINE.
        value_stride (int, optional): Width of plot stride. Defaults to 1.
        tooltip (str, optional): Tooltip to display over the Label. Defaults to "".

    Returns:
        Tuple(list(ui.Plot), list(AbstractValueModel)): ([plot_0, plot_1, plot_2], [val_model_x, val_model_y, val_model_z])
    """
    if len(value_names) == 3:
        # Add a default for the norm field name
        value_names = tuple(list(value_names) + [f"{''.join(value_names)}"])
    with ui.VStack(spacing=5):
        with ui.HStack():
            ui.Label(label, width=LABEL_WIDTH, alignment=ui.Alignment.LEFT_TOP, tooltip=tooltip)

            # Plots
            plot_height = LABEL_HEIGHT * 2 + 13
            plot_width = ui.Fraction(1)
            with ui.ZStack():
                ui.Rectangle(width=plot_width, height=plot_height)

                plot_0 = ui.Plot(
                    type,
                    min,
                    max,
                    *data[0],
                    value_stride=value_stride,
                    width=plot_width,
                    height=plot_height,
                    style=get_style()["PlotLabel::X"],
                )
                plot_1 = ui.Plot(
                    type,
                    min,
                    max,
                    *data[1],
                    value_stride=value_stride,
                    width=plot_width,
                    height=plot_height,
                    style=get_style()["PlotLabel::Y"],
                )
                plot_2 = ui.Plot(
                    type,
                    min,
                    max,
                    *data[2],
                    value_stride=value_stride,
                    width=plot_width,
                    height=plot_height,
                    style=get_style()["PlotLabel::Z"],
                )
                if include_norm:
                    plot_3 = ui.Plot(
                        type,
                        min,
                        max,
                        *np.linalg.norm(data, axis=1),
                        value_stride=value_stride,
                        width=plot_width,
                        height=plot_height,
                        style=get_style()["PlotLabel::W"]
                    )

            def update_min(model):
                plot_0.scale_min = model.as_float
                plot_1.scale_min = model.as_float
                plot_2.scale_min = model.as_float
                if include_norm:
                    plot_3.scale_min = model.as_float

            def update_max(model):
                plot_0.scale_max = model.as_float
                plot_1.scale_max = model.as_float
                plot_2.scale_max = model.as_float
                if include_norm:
                    plot_3.scale_max = model.as_float

            ui.Spacer(width=5)
            with ui.Frame(width=0):
                with ui.VStack(spacing=5):
                    max_model = ui.FloatDrag(
                        name="Field", width=40, alignment=ui.Alignment.LEFT_BOTTOM, tooltip="Max"
                    ).model
                    max_model.set_value(max)
                    min_model = ui.FloatDrag(
                        name="Field", width=40, alignment=ui.Alignment.LEFT_TOP, tooltip="Min"
                    ).model
                    min_model.set_value(min)

                    min_model.add_value_changed_fn(update_min)
                    max_model.add_value_changed_fn(update_max)
            ui.Spacer(width=20)

        # with ui.HStack():
        #     ui.Spacer(width=40)
        #     val_models = xyz_builder()#**{"args":args})

        field_labels = [(value_names[0], COLOR_X), (value_names[1], COLOR_Y), (value_names[2], COLOR_Z)]
        if include_norm:
            field_labels.append((value_names[3], (1,1,1,1)))
        RECT_WIDTH = 13
        # SPACING = 4
        with ui.HStack():
            ui.Spacer(width=LABEL_WIDTH )

            with ui.ZStack():
                value_label_width = ui.Fraction(1/5)
                with ui.HStack():
                    with ui.ZStack(width=RECT_WIDTH + 1):
                        ui.Rectangle(name="vector_label", style={"background_color": field_labels[0][1]})
                        ui.Label(field_labels[0][0], name="vector_label", alignment=ui.Alignment.CENTER)
                    val_model_x = ui.FloatDrag(
                        name="Field",
                        width=value_label_width,
                        height=LABEL_HEIGHT,
                        enabled=False,
                        alignment=ui.Alignment.LEFT_CENTER,
                        tooltip=value_names[0] + " Value",
                    ).model
                    ui.Spacer(width=4)
                    with ui.ZStack(width=RECT_WIDTH + 1):
                        ui.Rectangle(name="vector_label", style={"background_color": field_labels[1][1]})
                        ui.Label(field_labels[1][0], name="vector_label", alignment=ui.Alignment.CENTER)
                    val_model_y = ui.FloatDrag(
                        name="Field",
                        width=value_label_width,
                        height=LABEL_HEIGHT,
                        enabled=False,
                        alignment=ui.Alignment.LEFT_CENTER,
                        tooltip=value_names[1] + " Value",
                    ).model
                    ui.Spacer(width=4)
                    with ui.ZStack(width=RECT_WIDTH + 1):
                        ui.Rectangle(name="vector_label", style={"background_color": field_labels[2][1]})
                        ui.Label(field_labels[2][0], name="vector_label", alignment=ui.Alignment.CENTER)
                    val_model_z = ui.FloatDrag(
                        name="Field",
                        width=value_label_width,
                        height=LABEL_HEIGHT,
                        enabled=False,
                        alignment=ui.Alignment.LEFT_CENTER,
                        tooltip=value_names[2] + " Value",
                    ).model
                    if include_norm:
                        ui.Spacer(width=4)
                        with ui.ZStack(width=RECT_WIDTH + 1):
                            ui.Rectangle(name="vector_label", style={"background_color": field_labels[3][1]})
                            ui.Label(field_labels[3][0], name="vector_label", alignment=ui.Alignment.CENTER)
                        val_model_norm = ui.FloatDrag(
                            name="Field",
                            width=value_label_width,
                            height=LABEL_HEIGHT,
                            enabled=False,
                            alignment=ui.Alignment.LEFT_CENTER,
                            tooltip=value_names[3] + " Value",
                        ).model
                    ui.Spacer(width=20)


        add_separator()
        if include_norm:
            return [plot_0, plot_1, plot_2, plot_3], [val_model_x, val_model_y, val_model_z, val_model_norm]
        else:
            return [plot_0, plot_1, plot_2], [val_model_x, val_model_y, val_model_z]


def combo_floatfield_slider_builder(
    label="", type="floatfield_stringfield", default_val=0.5, min=0, max=1, step=0.01, tooltip=["", ""]
):
    """Creates a Stylized FloatField + FloatSlider Widget

    Args:
        label (str, optional): Label to the left of the UI element. Defaults to "".
        type (str, optional): Type of UI element. Defaults to "floatfield_stringfield".
        default_val (float, optional): Default Value. Defaults to 0.5.
        min (int, optional): Minimum Value. Defaults to 0.
        max (int, optional): Maximum Value. Defaults to 1.
        step (float, optional): Step. Defaults to 0.01.
        tooltip (list, optional): List of tooltips. Defaults to ["", ""].

    Returns:
        Tuple(AbstractValueModel, IntSlider): (flt_field_model, flt_slider_model)
    """
    with ui.HStack():
        ui.Label(label, width=LABEL_WIDTH, alignment=ui.Alignment.LEFT_CENTER, tooltip=tooltip[0])
        ff = ui.FloatField(
            name="Field", width=BUTTON_WIDTH / 2, alignment=ui.Alignment.LEFT_CENTER, tooltip=tooltip[1]
        ).model
        ff.set_value(default_val)
        ui.Spacer(width=5)
        fs = ui.FloatSlider(
            width=ui.Fraction(1), alignment=ui.Alignment.LEFT_CENTER, min=min, max=max, step=step, model=ff
        )

        add_line_rect_flourish(False)
        return ff, fs

def multi_cb_builder(
    label="",
    type="multi_checkbox",
    count=2,
    text=[" ", " "],
    default_val=[False, False],
    tooltip=["", "", ""],
    on_clicked_fn=[None, None],
):
    """Creates a Row of Stylized Checkboxes.

    Args:
        label (str, optional): Label to the left of the UI element. Defaults to "".
        type (str, optional): Type of UI element. Defaults to "multi_checkbox".
        count (int, optional): Number of UI elements to create. Defaults to 2.
        text (list, optional): List of text rendered on the UI elements. Defaults to [" ", " "].
        default_val (list, optional): List of default values. Checked is True, Unchecked is False. Defaults to [False, False].
        tooltip (list, optional): List of tooltips to display over the UI elements. Defaults to ["", "", ""].
        on_clicked_fn (list, optional): List of call-backs function when clicked. Defaults to [None, None].

    Returns:
        list(ui.SimpleBoolModel): List of models
    """
    cbs = []
    with ui.HStack():
        ui.Label(label, width=LABEL_WIDTH - 12, alignment=ui.Alignment.LEFT_CENTER, tooltip=tooltip[0])
        for i in range(count):
            cb = ui.SimpleBoolModel(default_value=default_val[i])
            callable = on_clicked_fn[i]
            if callable is None:
                callable = lambda x: None
            SimpleCheckBox(default_val[i], callable, model=cb)
            ui.Label(
                text[i], width=BUTTON_WIDTH / 2, alignment=ui.Alignment.LEFT_CENTER, tooltip=tooltip[i + 1]
            )
            if i < count - 1:
                ui.Spacer(width=5)
            cbs.append(cb)
        add_line_rect_flourish()
    return cbs

def combo_cb_dropdown_builder(
    label="",
    type="checkbox_dropdown",
    default_val=[False, 0],
    items=["Option 1", "Option 2", "Option 3"],
    tooltip="",
    on_clicked_fn=[lambda x: None, None],
):
    """Creates a Stylized Dropdown Combobox with an Enable Checkbox

    Args:
        label (str, optional): Label to the left of the UI element. Defaults to "".
        type (str, optional): Type of UI element. Defaults to "checkbox_dropdown".
        default_val (list, optional): list(cb_default, dropdown_default). Defaults to [False, 0].
        items (list, optional): List of items for dropdown box. Defaults to ["Option 1", "Option 2", "Option 3"].
        tooltip (str, optional): Tooltip to display over the Label. Defaults to "".
        on_clicked_fn (list, optional): List of callback functions. Defaults to [lambda x: None, None].

    Returns:
        Tuple(ui.SimpleBoolModel, ui.ComboBox): (cb_model, combobox)
    """
    with ui.HStack():
        ui.Label(label, width=LABEL_WIDTH - 12, alignment=ui.Alignment.LEFT_CENTER, tooltip=tooltip)
        cb = ui.SimpleBoolModel(default_value=default_val[0])
        SimpleCheckBox(default_val[0], on_clicked_fn[0], model=cb)
        combo_box = ui.ComboBox(
            default_val[1], *items, name="ComboBox", width=ui.Fraction(1), alignment=ui.Alignment.LEFT_CENTER
        )

        def on_clicked_wrapper(model, val):

            on_clicked_fn[1](items[model.get_item_value_model().as_int])

        combo_box.model.add_item_changed_fn(on_clicked_wrapper)

        add_line_rect_flourish(False)

        return cb, combo_box