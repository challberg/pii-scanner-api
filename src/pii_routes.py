from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.database import get_db
from src.deps import get_current_active_user
from src.models import User, SearchRequest
from src.pii_schemas import PIICreate, SearchResultResponse, SearchHistoryItem, SearchSource
from src.config import get_settings

limiter = Limiter(key_func=get_remote_address)
settings = get_settings()

router = APIRouter(prefix="/pii", tags=["pii"])


def perform_data_broker_search(search_request: SearchRequest, db: Session) -> None:
    pass


@router.post("/scan", response_model=SearchResultResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def submit_pii_scan(
    request: Request,
    pii_data: PIICreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    search_request = SearchRequest(
        user_id=current_user.id,
        first_name=pii_data.first_name,
        last_name=pii_data.last_name,
        email=pii_data.email,
        phone=pii_data.phone,
        address=pii_data.address,
        city=pii_data.city,
        state=pii_data.state,
        zip_code=pii_data.zip_code,
        status="pending"
    )
    db.add(search_request)
    db.commit()
    db.refresh(search_request)

    return SearchResultResponse(
        id=search_request.id,
        first_name=search_request.first_name,
        last_name=search_request.last_name,
        email=search_request.email,
        phone=search_request.phone,
        address=search_request.address,
        created_at=search_request.created_at.isoformat(),
        sources=[]
    )


@router.get("/searches", response_model=list[SearchHistoryItem])
@limiter.limit("20/minute")
def list_searches(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    searches = (
        db.query(SearchRequest)
        .filter(SearchRequest.user_id == current_user.id)
        .order_by(SearchRequest.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        SearchHistoryItem(
            id=s.id,
            first_name=s.first_name,
            last_name=s.last_name,
            created_at=s.created_at.isoformat(),
            result_count=len(s.sources)
        )
        for s in searches
    ]


@router.get("/searches/{search_id}", response_model=SearchResultResponse)
@limiter.limit("20/minute")
def get_search_result(
    request: Request,
    search_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    search_request = (
        db.query(SearchRequest)
        .filter(
            SearchRequest.id == search_id,
            SearchRequest.user_id == current_user.id
        )
        .first()
    )

    if not search_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search request not found"
        )

    return SearchResultResponse(
        id=search_request.id,
        first_name=search_request.first_name,
        last_name=search_request.last_name,
        email=search_request.email,
        phone=search_request.phone,
        address=search_request.address,
        created_at=search_request.created_at.isoformat(),
        sources=[
            SearchSource(
                source_name=s.source_name,
                source_url=s.source_url,
                data_found=s.data_found,
                data_details=s.data_details
            )
            for s in search_request.sources
        ]
    )