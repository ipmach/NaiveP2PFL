
from dataclasses import dataclass
import typing as t


@dataclass
class Status:
    active: str = "active"
    unactive: str = "unactive"
    
    start_training: str = "start_training"
    doing_training: str = "doing_training"

    current_version: int = 1


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


@dataclass
class Config:
    node_id: str
    node_type: str

    current_version: int = 1
    current_status: str = Status.active


class Backend:
    def __init__(
        self, config=Config(node_id="default", node_type="backend")
    ) -> None:
        self.config = config
        self.pwd = "helloworld"

    def get_status(self) -> t.Tuple[t.Dict[str, str], HttpStatus]:
        return self.config.__dict__, HttpStatus.ok
    
    def command(self, cmd: str, pwd: str) -> t.Tuple[str, HttpStatus]:
        if pwd != self.pwd:
            return f"Invalid password: {pwd}", HttpStatus.forbidden

        if cmd == Commands.start:
            self.config.current_status = Status.active
        elif cmd == Commands.stop:
            self.config.current_status = Status.unactive
        elif cmd == Commands.train:
            self.config.current_status = Status.start_training
        else:
            raise ValueError(f"Unknown command: {cmd}")
        return "Done", HttpStatus.ok