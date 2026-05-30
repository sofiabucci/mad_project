Converts the output of rectParts.c into Prolog fact files.

Input format:
  <num_instances>
  For each instance:
    <num_rectangles>
    <face_id> <num_verts> <x1> <y1> <x2> <y2> ... <xn> <yn>
    ...

Output: one .pl file per instance, e.g. instance_1.pl, instance_2.pl, ...

Each file contains:
  retangulo(r1, [1, 2, ..., n]).
  ...
where vertex identifiers are assigned globally per instance
(same coordinates → same identifier).

Usage:

python3 convert_to_prolog.py <input_file> [output_prefix]

input_file     : file with the C program output
output_prefix  : prefix for output files (default: "instance")
                   produces instance_1.pl, instance_2.pl, ...