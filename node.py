
import typing as t

from config import Commands, Config, HttpStatus, Status


status_changes = {
    Commands.start: Status.active,
    Commands.stop: Status.unactive,
    Commands.train: Status.start_training,
}


def _status_logic(config: Config, new_status: Commands) -> t.Tuple[str, HttpStatus]:
    new_status = status_changes.get(new_status, None)
    
    if config.current_status == new_status:
        return f"Already in status: {new_status}", HttpStatus.ok
    elif config.current_status == Status.active:
        config.current_status = new_status
        return "Done", HttpStatus.ok
    elif config.current_status == Status.doing_training:
        return "Cannot change status while training", HttpStatus.forbidden
    elif config.current_status == Status.unactive:
        if new_status == Status.active:
            config.current_status = new_status
            return "Done", HttpStatus.ok
        else:
            return "Cannot change status from unactive", HttpStatus.forbidden
    else:
        return "Unknow change", HttpStatus.forbidden


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
        return _status_logic(self.config, new_status=cmd)