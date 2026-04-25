from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    search_requests = relationship("SearchRequest", back_populates="user")


class SearchRequest(Base):
    __tablename__ = "search_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(2), nullable=True)
    zip_code = Column(String(10), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="pending")

    user = relationship("User", back_populates="search_requests")
    sources = relationship("SearchSource", back_populates="search_request")


class SearchSource(Base):
    __tablename__ = "search_sources"

    id = Column(Integer, primary_key=True, index=True)
    search_request_id = Column(Integer, ForeignKey("search_requests.id"), nullable=False)
    source_name = Column(String(255), nullable=False)
    source_url = Column(Text, nullable=True)
    data_found = Column(Boolean, default=False)
    data_details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    search_request = relationship("SearchRequest", back_populates="sources")