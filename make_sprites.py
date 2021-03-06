import subprocess
import tempfile
from PIL import Image
import sys

DEST_FILENAME = 'sprites.png'
SRC_FILENAME = 'sprites.svg'

TILE_SIZE = 64
MARGIN = 8
TILE_SIZE2 = TILE_SIZE + MARGIN*2

MAP = {
    (0, 0): (0, 1, None),
    (1, 0): (0, 0, Image.ROTATE_180),
    (2, 0): (0, 0, None),
    (3, 0): (0, 0, Image.ROTATE_90),
    (4, 0): (0, 0, Image.ROTATE_270),
    (5, 0): (0, 1, None),
    (6, 0): (0, 1, None),

    (0, 1): (2, 0, Image.ROTATE_180),
    (1, 1): (1, 0, None),
    (2, 1): (1, 0, None),
    (3, 1): (3, 1, Image.ROTATE_270),
    (4, 1): (3, 1, Image.ROTATE_180),
    (5, 1): (3, 0, Image.ROTATE_90),
    (6, 1): (2, 1, None),

    (0, 2): (2, 0, None),
    (1, 2): (1, 0, None),
    (2, 2): (1, 0, None),
    (3, 2): (3, 1, None),
    (4, 2): (3, 1, Image.ROTATE_90),
    (5, 2): (3, 0, Image.ROTATE_270),
    (6, 2): (2, 1, Image.ROTATE_180),

    (0, 3): (2, 0, Image.ROTATE_90),
    (1, 3): (3, 1, Image.ROTATE_90),
    (2, 3): (3, 1, Image.ROTATE_180),
    (3, 3): (1, 0, Image.ROTATE_90),
    (4, 3): (1, 0, Image.ROTATE_90),
    (5, 3): (3, 0, None),
    (6, 3): (2, 1, Image.ROTATE_270),

    (0, 4): (2, 0, Image.ROTATE_270),
    (1, 4): (3, 1, None),
    (2, 4): (3, 1, Image.ROTATE_270),
    (3, 4): (1, 0, Image.ROTATE_90),
    (4, 4): (1, 0, Image.ROTATE_90),
    (5, 4): (3, 0, Image.ROTATE_180),
    (6, 4): (2, 1, Image.ROTATE_90),

    (0, 5): (1, 1, None),
}

with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = tmpdir + '/tmp.png'
    subprocess.run(['inkscape',
                    '--export-png', tmp_path,
                    '--export-width', str(TILE_SIZE*4),
                    '--export-height', str(TILE_SIZE*2),
                    SRC_FILENAME],
                   check=True)

    src = Image.open(tmp_path).transpose(Image.FLIP_TOP_BOTTOM)

dest = Image.new('RGBA', (TILE_SIZE2*7, TILE_SIZE2*6), color=(0, 0, 0, 0))

for (x, y), (u, v, r) in MAP.items():
    src_box = (u*TILE_SIZE, v*TILE_SIZE, (u+1)*TILE_SIZE, (v+1)*TILE_SIZE)
    src_crop = src.crop(src_box)
    if r is not None:
        src_crop = src_crop.transpose(r)
    for dx, dy in (1, 0), (-1, 0), (0, 1), (0, -1):
        for i in range(MARGIN, -1, -1):
            dest.paste(src_crop, (x*TILE_SIZE2+dx*i+MARGIN,
                                  y*TILE_SIZE2+dy*i+MARGIN))

dest.transpose(Image.FLIP_TOP_BOTTOM).save(DEST_FILENAME)

print('Output saved to', DEST_FILENAME, file=sys.stderr)
