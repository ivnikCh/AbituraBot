class App:
    """A class for storing information about the application for submission of documents"""

    def __init__(
        self,
        pass_id: str,
        url_docs: str,
        name_program: str,
        state: str,
        comment: str,
        is_delete: bool,
    ):
        self.pass_id = pass_id
        self.url_docs = url_docs
        self.name_program = name_program
        self.state = state
        self.comment = comment
        self.is_delete = is_delete

    @classmethod
    def from_json(cls, data: dict):
        """Converts from json to a class object"""
        return cls(
            data["pass_id"],
            data["url_docs"],
            data["name_program"],
            data["state"],
            data["comment"],
            data["is_delete"],
        )

    def to_json(self) -> dict:
        """Converts from class object to a json"""
        return {
            "pass_id": self.pass_id,
            "url_docs": self.url_docs,
            "name_program": self.name_program,
            "state": self.state,
            "comment": self.comment,
            "is_delete": self.is_delete,
        }

    def to_str(self) -> str:
        """Return info about application"""
        res = (
            "url for docs "
            + self.url_docs
            + "\n name program - "
            + self.name_program
            + "\n state: "
            + self.state
            + "\n"
            + self.comment
        )
        return res
