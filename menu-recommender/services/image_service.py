import replicate
import tempfile
import os

from fastapi.responses import FileResponse

class ImageService:
    def generate_image(self, name: str) -> FileResponse:
        input = {
            "width": 512,
            "height": 512,
            "prompt": f"a mouthwatering plate of {name}",
            "checkpoint": "ProteusV0.4.safetensors"
        }

        filename_prefix = name.strip().lower().replace(" ", "_")
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, f"{filename_prefix}.webp")

        if not os.path.exists(file_path):
            output = replicate.run(
                "fofr/ays-text-to-image:a004c3ac8f62ac95a90b5a0c264beb47b66a6d1f8141b76fb27cd90e9a8bfe8e",
                input=input
            )

            for index, item in enumerate(output):
                with open(file_path, "wb") as f:
                    f.write(item.read())

        return FileResponse(path=file_path, filename=f"{filename_prefix}.webp", media_type="image/webp")
