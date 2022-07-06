from fastapi import APIRouter
from tbay import root, threads, settings
from qbittorrent import root as qbittorrent

router = APIRouter()

# TBayMod
router.include_router(threads.router)
router.include_router(root.router)
router.include_router(settings.router)

# qBittorrent
router.include_router(qbittorrent.router)
