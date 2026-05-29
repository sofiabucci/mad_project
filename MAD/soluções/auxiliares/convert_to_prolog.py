#!/usr/bin/env python3
"""
Converts the output of rectParts.c into Prolog fact files.

Input format:
  <num_instances>
  For each instance:
    <num_rectangles>
    <face_id> <num_verts> <x1> <y1> <x2> <y2> ... <xn> <yn>
    ...

Output: one .pl file per instance, e.g. instance_1.pl, instance_2.pl, ...

Each file contains:
  retangulo(r1, [v1, v2, ..., vn]).
  ...
where vertex identifiers are assigned globally per instance
(same coordinates → same identifier).

Usage:
  python3 convert_to_prolog.py <input_file> [output_prefix]

  input_file     : file with the C program output
  output_prefix  : prefix for output files (default: "instance")
                   produces instance_1.pl, instance_2.pl, ...
"""

import sys
import os


def parse_and_convert(input_path, output_prefix="instance"):
    with open(input_path, "r") as f:
        tokens = f.read().split()

    pos = 0

    def read_int():
        nonlocal pos
        val = int(tokens[pos])
        pos += 1
        return val

    num_instances = read_int()

    for inst_idx in range(1, num_instances + 1):
        num_rects = read_int()

        # Maps (x, y) -> vertex id, assigned in order of first appearance
        coord_to_id = {}
        next_id = [1]

        def get_vertex_id(x, y):
            key = (x, y)
            if key not in coord_to_id:
                coord_to_id[key] = next_id[0]
                next_id[0] += 1
            return coord_to_id[key]

        rectangles = []  # list of (rect_id, [vertex_ids])

        for _ in range(num_rects):
            face_id = read_int()
            num_verts = read_int()
            vertex_ids = []
            for _ in range(num_verts):
                x = read_int()
                y = read_int()
                vertex_ids.append(get_vertex_id(x, y))
            rectangles.append((face_id, vertex_ids))

        # Write .pl file
        out_path = f"{output_prefix}_{inst_idx}.pl"
        with open(out_path, "w") as out:
            out.write(f"% Prolog facts for instance {inst_idx}\n")
            out.write(f"% {num_rects} rectangles, "
                      f"{next_id[0]-1} unique vertices\n\n")

            for face_id, vids in rectangles:
                vlist = ", ".join(str(v) for v in vids)
                out.write(f"retangulo(r{face_id}, [{vlist}]).\n")

        print(f"  Instance {inst_idx}: {num_rects} rectangles, "
              f"{next_id[0]-1} unique vertices → {out_path}")

    print(f"\nDone. {num_instances} file(s) generated.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 convert_to_prolog.py <input_file> [output_prefix]")
        sys.exit(1)

    input_file = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) >= 3 else "instance"

    if not os.path.exists(input_file):
        print(f"Error: file '{input_file}' not found.")
        sys.exit(1)

    print(f"Reading: {input_file}")
    parse_and_convert(input_file, prefix)
