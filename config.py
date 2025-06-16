

from dataclasses import dataclass


@dataclass
class Status:
    active: str = "active"
    unactive: str = "unactive"

    start_training: str = "start_training"
    doing_training: str = "doing_training"

    current_version: int = 1


@dataclass
class Config:
    node_id: str
    node_type: str

    current_version: int = 1
    current_status: str = Status.active


@dataclass
class HttpStatus:
    ok: str = "200 OK"
    not_found: str = "404 Not Found"
    internal_error: str = "500 Internal Server Error"
    forbidden: str = "403 Forbidden"


@dataclass
class Commands:
    start: str = "start"
    stop: str = "stop"
    train: str = "train"