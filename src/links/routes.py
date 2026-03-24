from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl

from links.schemas import LinkResponse, ShortIdResponse
from links.services import LinkService, get_link_service
from links.exceptions import LinkIntegrityError


router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/stats/{short_id}")
def stats(
    short_id: str,
    link_service: LinkService = Depends(get_link_service)
) -> LinkResponse:
    link = link_service.get_link(short_id)
    if not link:
        raise HTTPException(404, "Not found")

    return LinkResponse(
        short_id=link.short_id,
        original_url=link.original_url,
        clicks=link.clicks,
    )


@router.get("/shorten")
def shorten(
    url: HttpUrl,
    link_service: LinkService = Depends(get_link_service)
) -> ShortIdResponse:
    try:
        link = link_service.shorten(str(url))
    except LinkIntegrityError as e:
        raise HTTPException(400, str(e))

    return ShortIdResponse(short_id=link.short_id)


@router.get("/{short_id}")
def redirect(
    short_id: str,
    link_service: LinkService = Depends(get_link_service)
) -> RedirectResponse:
    link = link_service.get_link(short_id)
    if not link:
        raise HTTPException(404, "Not found")

    link_service.increment_clicks(link)

    return RedirectResponse(link.original_url)

