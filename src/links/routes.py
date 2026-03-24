from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from links.schemas import LinkCreate, LinkResponse, ShortIdResponse
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


@router.post("/shorten")
def shorten(
    data: LinkCreate,
    link_service: LinkService = Depends(get_link_service)
) -> ShortIdResponse:
    try:
        short_url = link_service.shorten(str(data.url))
    except LinkIntegrityError as e:
        raise HTTPException(400, str(e))

    return ShortIdResponse(short_url=short_url)


@router.get("/{short_id}")
def redirect(
    short_id: str,
    link_service: LinkService = Depends(get_link_service)
) -> RedirectResponse:
    url = link_service.get_original_url(short_id)
    if not url:
        raise HTTPException(404, "Not found")

    return RedirectResponse(url)

