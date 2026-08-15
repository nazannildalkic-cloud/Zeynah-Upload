"""Zeynah-Logo: aus der Kugel im Video herauswachsen und rausschweben."""
import subprocess
from PIL import Image, ImageFilter, ImageDraw
import imageio_ffmpeg

W, H, FPS = 1920, 1080, 24
DUR = 5.04
exe = imageio_ffmpeg.get_ffmpeg_exe()

# --- Logo: sauberes Chrom-Z ohne Schattenkasten ---
logo = Image.open('assets/zeynah-z-klein.png').convert('RGBA')
LW, LH = logo.size
print('Logo-Z:', LW, 'x', LH)

def smooth(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)

# Kugel-Mitte wandert leicht (Kamera-Zoom im Video): Anfang -> Ende
def sphere_center(t):
    p = min(t / 4.5, 1.0)
    return 905 + 55 * p, 730 + 65 * p

dec = subprocess.Popen(
    [exe, '-loglevel', 'error', '-i', 'hero.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'],
    stdout=subprocess.PIPE)
enc = subprocess.Popen(
    [exe, '-y', '-loglevel', 'error',
     '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0',
     '-i', 'hero.mp4', '-map', '0:v', '-map', '1:a?',
     '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p',
     '-c:a', 'copy', '-movflags', '+faststart', 'hero_kugel.mp4'],
    stdin=subprocess.PIPE)

n = 0
frame_bytes = W * H * 3
while True:
    raw = dec.stdout.read(frame_bytes)
    if len(raw) < frame_bytes:
        break
    t = n / FPS
    frame = Image.frombuffer('RGB', (W, H), raw).convert('RGBA')

    # Animationskurve: einblenden -> wachsen, diagonal nach links oben
    # rausschweben -> am Ende sanft ausblenden (sauberer Loop)
    if t < 0.4:
        alpha = 0.0
    elif t < 1.2:
        alpha = (t - 0.4) / 0.8                    # 0.4s-1.2s einblenden
    elif t < 4.4:
        alpha = 1.0
    else:
        alpha = max(0.0, 1.0 - (t - 4.4) / 0.6)    # 4.4s-5.0s ausblenden
    grow = smooth((t - 1.0) / 3.4)                  # 1.0s-4.4s wachsen/schweben
    size = 60 + grow * 320                          # 60px -> 380px breit
    cx, cy = sphere_center(t)
    x = cx + (350 - cx) * grow                      # diagonal nach links oben
    y = (cy - 20) + (260 - (cy - 20)) * grow        # auf die freie Wandflaeche

    if alpha > 0.01:
        lw = max(2, int(size))
        lh = max(2, int(size * LH / LW))
        lg = logo.resize((lw, lh), Image.LANCZOS)
        # Glow mit Rand-Puffer, damit die Weichzeichnung nicht abgeschnitten wird
        pad = max(10, lw // 3)
        gl = Image.new('RGBA', (lw + 2 * pad, lh + 2 * pad), (0, 0, 0, 0))
        gd = ImageDraw.Draw(gl)
        gd.bitmap((pad, pad), lg.split()[3], fill=(76, 155, 240, 200))
        gl = gl.filter(ImageFilter.GaussianBlur(max(6, lw // 10)))
        if alpha < 1.0:
            for im in (lg, gl):
                a = im.split()[3].point(lambda v: int(v * alpha))
                im.putalpha(a)
        px, py = int(x - lw / 2), int(y - lh / 2)
        frame.alpha_composite(gl, (px - pad, py - pad))  # Glow dahinter
        frame.alpha_composite(lg, (px, py))              # Logo

    enc.stdin.write(frame.convert('RGB').tobytes())
    n += 1

enc.stdin.close()
enc.wait()
dec.wait()
print(f'Fertig: {n} Frames -> hero_kugel.mp4')
