from __future__ import annotations

import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.config import Settings
from app.models import RetrievedChunks