from application import App


class User:
    """Class with user information"""

    MAX_APP = 5

    def __init__(self):
        self.count_apps = 0
        self.app_id = None
        self.apps = []

    def to_json(self) -> dict:
        """Converts from class object to a json"""
        return {
            "app_id": self.app_id,
            "apps": [i.to_json() for i in self.apps],
        }

    @classmethod
    def from_json(cls, data: dict):
        """Converts from json to a class object"""
        res = cls()
        res.app_id = data["app_id"]
        res.apps = [App.from_json(i) for i in data["apps"]]
        return res

    def add_app(
        self,
        pass_id: str,
        url_docs: str,
        name_program: str,
        state: str,
        comment: str,
    ):
        """Add application in list"""
        if self.count_apps + 1 < User.MAX_APP:
            self.apps.append(
                App(pass_id, url_docs, name_program, state, comment, False)
            )

    def delete_app(self, app_id):
        """Delete application in list"""
        self.apps[app_id].is_delete = True
        self.count_apps -= 1

    def to_str(self) -> str:
        """Convert data to str"""
        ret = []
        it_id = 0
        for i in self.apps:
            if not (i.is_delete):
                ret.append('/' + str(it_id) + 'Application\n' + i.to_str())
            it_id += 1
        return "\n\n\n".join(ret)
