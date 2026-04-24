"""
Generates a circuit-board style SVG backdrop.

Produces orthogonal traces on a 40px grid with small circular pads at the
endpoints and bends. Colour + stroke width chosen to sit at low opacity
behind the social-preview content without competing with the typography.
"""
import random
import math

# Fixed seed so each regeneration looks the same - deterministic background.
random.seed(42)

WIDTH, HEIGHT = 1280, 640
GRID = 40
NUM_TRACES = 55
TRACE_COLOUR = "#818cf8"

def generate():
    lines = []
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
        f'height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">'
    )
    lines.append(
        f'<g stroke="{TRACE_COLOUR}" stroke-width="1.3" fill="none" '
        f'stroke-linecap="round" stroke-linejoin="round">'
    )

    pads = set()
    for _ in range(NUM_TRACES):
        # Start at a random grid point inside the canvas, not on the edge
        x = random.randint(2, WIDTH // GRID - 2) * GRID
        y = random.randint(2, HEIGHT // GRID - 2) * GRID

        d = f"M {x} {y}"
        pads.add((x, y))

        # 2-6 segments, alternating horizontal/vertical so traces stay
        # on a PCB-like grid (no diagonals)
        segs = random.randint(2, 6)
        horizontal = random.random() < 0.5
        for _ in range(segs):
            if horizontal:
                dx = random.choice([-1, 1]) * GRID * random.randint(1, 5)
                new_x = max(GRID, min(WIDTH - GRID, x + dx))
                d += f" L {new_x} {y}"
                x = new_x
            else:
                dy = random.choice([-1, 1]) * GRID * random.randint(1, 4)
                new_y = max(GRID, min(HEIGHT - GRID, y + dy))
                d += f" L {x} {new_y}"
                y = new_y
            pads.add((x, y))
            horizontal = not horizontal

        lines.append(f'<path d="{d}"/>')

    lines.append("</g>")

    # Small circular pads at every turn + endpoint. Slightly brighter so
    # they read as 'nodes' rather than disappearing into the traces.
    lines.append(f'<g fill="{TRACE_COLOUR}">')
    for (x, y) in pads:
        lines.append(f'<circle cx="{x}" cy="{y}" r="2.4"/>')
    lines.append("</g>")

    # A handful of larger 'component' rectangles for visual interest -
    # mimics IC packages on a real PCB.
    lines.append(f'<g fill="none" stroke="{TRACE_COLOUR}" stroke-width="1.2">')
    for _ in range(6):
        cx = random.randint(4, WIDTH // GRID - 5) * GRID
        cy = random.randint(3, HEIGHT // GRID - 4) * GRID
        w = random.choice([2, 3]) * GRID
        h = random.choice([2, 3]) * GRID
        lines.append(
            f'<rect x="{cx - w // 2}" y="{cy - h // 2}" '
            f'width="{w}" height="{h}" rx="3"/>'
        )
    lines.append("</g>")

    lines.append("</svg>")
    return "\n".join(lines)


if __name__ == "__main__":
    out = generate()
    with open("circuit.svg", "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Wrote circuit.svg - {len(out)} bytes")
