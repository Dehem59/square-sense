import uuid
from pathlib import Path

from core.dao.in_memory import InMemoryDAO
from core.dao.json_document import JsonDocumentDAO

USED_DAO_CLASS = JsonDocumentDAO
DB_PATH = str(Path(__file__).parent.parent / "data/people_counter.json")
ID_GENERATOR = uuid.uuid4
