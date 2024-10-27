import esbuild
from csscompressor import compress
import sass
from typing import Dict, Any


class AssetProcessor:
    """Base class for asset processors"""

    async def process(self, content: str, options: Dict[str, Any]) -> str:
        raise NotImplementedError


class JavaScriptProcessor(AssetProcessor):
    async def process(self, content: str, options: Dict[str, Any]) -> str:
        result = await esbuild.transform(
            content,
            sourcemap=options.get("sourcemaps", True),
            minify=options.get("minify", True),
            target="es2020",
            format="esm",
        )
        return result["code"]


class CSSProcessor(AssetProcessor):
    async def process(self, content: str, options: Dict[str, Any]) -> str:
        # Process SASS/SCSS if needed
        if options.get("file_type") in [".scss", ".sass"]:
            content = sass.compile(string=content)

        if options.get("minify", True):
            return compress(content)
        return content
