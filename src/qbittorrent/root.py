from typing import Dict
import base64
from pathlib import Path

from fastapi import APIRouter, Request
import qbittorrentapi
from qbittorrentapi import LoginFailed, APIConnectionError


router = APIRouter(
    prefix="/qbit",
    tags=["qBitTorrent"],
    responses={404: {"description": "Not found"}},
)

qbt_client = qbittorrentapi.Client(
    host='192.168.21.5',
    port=8084,
    username='admin',
    password='VeniVidiCacas',
)


@router.get("/")
async def is_alive():
    return {"success": True}


@router.post("/magnet")
async def add_magnet(body: Dict):
    try:
        category = body['category'] if 'category' in body else None
        qbt_client.torrents_add(urls=[body['magnet']], is_paused=False, use_auto_torrent_management=True, category=category)
        return {"success": True}
    except (Exception, LoginFailed, APIConnectionError) as error:
        return {"err": error}


# Make a TorrentDay specific endpoint
@router.post("/torrent-kjdfkjkd")
async def add_torrent(request: Request):#, name: str = '', fromUrl: str = '', category: str = ''):
    try:
        params = request.query_params

        if 'name' not in params and 'fromUrl' not in params:
            return {"err": 'Invalid name'}

        if 'fromUrl' in params:
            name = Path(params['fromUrl']).name
        else:
            name = params['name']

        if not name:
            return {"err": 'Invalid name'}
        category = params['category'] if 'category' in params else None
        tor: bytes = await request.body()
        # f = open(f'./{name}', 'wb')
        # f.write(tor)
        # f.close()
        qbt_client.torrents_add(torrent_files=tor, rename=name, is_paused=False, use_auto_torrent_management=True, category=category)
        return {"success": True}
    except (Exception, LoginFailed, APIConnectionError) as error:
        return {"err": error}

