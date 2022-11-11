import os
import uuid
from fastapi import UploadFile, HTTPException
from typing import List, Tuple
from core.config import BASE_DIR


class Handle_file_upload:
    def __init__(self, resource: str):
        self._img_dir = os.path.join(BASE_DIR, "static", resource)
        self._resource = resource

    async def handle_file(self, file: UploadFile) -> str:
        _, ext = os.path.splitext(file.filename)
        if not os.path.exists(self._img_dir):
            os.makedirs(self._img_dir)
        content = await file.read()
        file_name = f'{uuid.uuid4().hex}{ext}'
        with open(os.path.join(self._img_dir, file_name), mode='wb') as f:
            f.write(content)
        return os.path.join("/static", self._resource, file_name)

    async def handle_many_files_saver(self, file: List[UploadFile]):
        urls = {}
        for f in file:
            ext = f.content_type.split("/")[0]
            urls[ext] = await self.handle_file(file=f)
        return urls
