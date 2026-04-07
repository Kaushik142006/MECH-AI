import gradio as gr
from build123d import *
import os

# ----------------------------
# CAD FUNCTION
# ----------------------------
def create_nut(inner_dia, outer_dia, thickness):
    with BuildPart() as nut:
        with BuildSketch():
            RegularPolygon(radius=outer_dia / 2, side_count=6)
        extrude(amount=thickness)

        with BuildSketch(Plane.XY.offset(thickness)):
            Circle(radius=inner_dia / 2)
        extrude(amount=-thickness, mode=Mode.SUBTRACT)

    return nut


# ----------------------------
# GENERATE + RETURN STL
# ----------------------------
def generate_model(inner_dia, outer_dia, thickness):
    try:
        print("Generating model...")

        result = create_nut(inner_dia, outer_dia, thickness)

        file_path = "nut.stl"

        # Delete old file if exists
        if os.path.exists(file_path):
            os.remove(file_path)

        # Export STL
        export_stl(result.part, file_path)

        # Check file exists
        if not os.path.exists(file_path):
            raise Exception("STL file not created")

        print("Saved at:", os.path.abspath(file_path))

        return file_path

    except Exception as e:
        print("ERROR:", e)
        return None


# ----------------------------
# GRADIO UI
# ----------------------------
demo = gr.Interface(
    fn=generate_model,
    inputs=[
        gr.Number(label="Inner Diameter", value=30),
        gr.Number(label="Outer Diameter", value=50),
        gr.Number(label="Thickness", value=20),
    ],
    outputs=gr.Model3D(label="3D Model"),
    title="Nut Generator (360° View)"
)

# ----------------------------
# RUN
# ----------------------------
demo.launch(inbrowser=True)