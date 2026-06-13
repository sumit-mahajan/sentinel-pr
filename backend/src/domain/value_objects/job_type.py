from enum import Enum


class JobType(str, Enum):
    REVIEW = "review"
    EMBEDDING_CLEANUP = "embedding_cleanup"
