from .core import FastHTMLBundler
from watchfiles import awatch
import logging

__all__ = ["DevServer"]


class DevServer:
    def __init__(self, bundler: FastHTMLBundler):
        self.bundler = bundler
        self.logger = logging.getLogger("FastHTMLBundler")

    async def start(self):
        """Start development server with hot reloading"""
        if not self.bundler.config.dev_mode:
            return

        self.logger.info("Starting development server...")
        async for changes in awatch(self.bundler.config.entry_dir):
            await self.handle_changes(changes)

    async def handle_changes(self, changes):
        """Handle file changes and trigger rebuilds"""
        for change_type, path in changes:
            self.logger.info(f"Change detected: {path}")
            await self.bundler.asset_manager.rebuild_changed([(change_type, path)])
