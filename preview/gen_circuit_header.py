"""
Generates a 1500x500 circuit backdrop for the X/Twitter header.
Same aesthetic as the GitHub social preview but wider-short aspect.
"""
import random

random.seed(73)  # Different seed = different trace layout from the 1280x640 version

WIDTH, HEIGHT = 1500, 500
GRID = 40
NUM_TRACES = 50
TRACE_COLOUR = "#818cf8"

def generate():
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
        f'height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        f'<g stroke="{TRACE_COLOUR}" stroke-width="1.3" fill="none" '
        f'stroke-linecap="round" stroke-linejoin="round">'
    ]

    pads = set()
    for _ in range(NUM_TRACES):
        x = random.randint(2, WIDTH // GRID - 2) * GRID
        y = random.randint(2, HEIGHT // GRID - 2) * GRID
        d = f"M {x} {y}"
        pads.add((x, y))
        segs = random.randint(2, 6)
        horizontal = random.random() < 0.5
        for _ in range(segs):
            if horizontal:
                dx = random.choice([-1, 1]) * GRID * random.randint(1, 5)
                new_x = max(GRID, min(WIDTH - GRID, x + dx))
                d += f" L {new_x} {y}"
                x = new_x
            else:
                dy = random.choice([-1, 1]) * GRID * random.randint(1, 3)
                new_y = max(GRID, min(HEIGHT - GRID, y + dy))
                d += f" L {x} {new_y}"
                y = new_y
            pads.add((x, y))
            horizontal = not horizontal
        lines.append(f'<path d="{d}"/>')

    lines.append("</g>")

    lines.append(f'<g fill="{TRACE_COLOUR}">')
    for (x, y) in pads:
        lines.append(f'<circle cx="{x}" cy="{y}" r="2.4"/>')
    lines.append("</g>")

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
    with open("circuit-header.svg", "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Wrote circuit-header.svg - {len(out)} bytes")
