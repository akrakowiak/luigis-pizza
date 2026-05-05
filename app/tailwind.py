import subprocess

from app.config import settings


def run_tailwind(dev: bool) -> None:
    in_path = settings.STATIC_DIR / "tailwind-config.css"
    out_path = settings.STATIC_DIR / "tailwind.css"

    if dev:
        subprocess.Popen(["tailwindcss", "-i", in_path, "-o", out_path, "--watch"])
    else:
        subprocess.run(["tailwindcss", "-i", in_path, "-o", out_path, "--minify"])
