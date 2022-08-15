from .base import Base


class Runner(Base):
    
    def __init__(
        self, 
        platform: str, 
        hostname: str = None, 
        username: str = None, 
        password: str = None, 
        verify_ssl: bool = False, 
        ssh_key_path: str = None, 
        private_key_string: str = None, 
        ssh_port: int = 22, 
        ssh_timeout: int = 5,
    ):
        if platform.lower() not in ["macos", "linux", "windows", "aws"]:
            raise Exception()
        Base.platform = platform.lower()
        Base._run_type = "remote" if hostname else "local"
        Base.hostname = hostname
        Base.username = username
        Base.password = password
        Base.verify_ssl = verify_ssl
        Base.ssh_key_path = ssh_key_path
        Base.private_key_string = private_key_string
        Base.ssh_port = ssh_port
        Base.ssh_timeout = ssh_timeout

    def run(self, command: str, executor: str, cwd: str = None, elevation_required: bool = False):
        if Base._run_type == "local":
            pass
        else:
            pass

    def copy(self):
        pass

