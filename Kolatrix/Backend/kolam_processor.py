import cv2
import numpy as np
import svgwrite
from pathlib import Path


def process_kolam(image_path: str, output_path: str, svg_path: str):
    # Load image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Invalid image")

    height, width = img.shape[:2]   # <-- get image size

    # Preprocessing: blur + edge detection
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Prepare color output image
    output = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Draw smoothed contours
    smooth_contours = []
    for cnt in contours:
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        cv2.drawContours(output, [approx], -1, (0, 0, 255), 2)
        smooth_contours.append(approx)

    # Save processed raster output
    cv2.imwrite(output_path, output)

    # Save as SVG (vector format) with correct size
    dwg = svgwrite.Drawing(svg_path, size=(f"{width}px", f"{height}px"))
    for cnt in smooth_contours:
        points = [(int(x), int(y)) for [x, y] in cnt.reshape(-1, 2)]
        dwg.add(dwg.polyline(points, stroke="black", fill="none", stroke_width=2))
    dwg.save()

    return output_path, svg_path
