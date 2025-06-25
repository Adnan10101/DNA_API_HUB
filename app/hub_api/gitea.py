import gogs_client
import hub_api.environment as env
from json import loads
from base64 import b64encode


class GitWrapper():
    gogs_token = gogs_client.Token(env.GITEA_TOKEN)
    
    def get_repo(self):
        api = gogs_client.GogsApi(env.GITEA_API_URL)
        repo = api.get_user_repos(self.gogs_token, env.REPO_NAME)
        if not api.repo_exists(self.gogs_token, env.REPO_OWNER, env.REPO_NAME):
            print("Repository does not exist")
        else:
            repo = api.lookup_repo(self.gogs_token, env.REPO_OWNER, env.REPO_NAME)
            if repo.fork:
                print("Repository is a fork")
            else:
                print("Repository is not a fork")
        
    def create_file(self, yaml, pv_file_name, FILE_PATH, REPO_NAME):
        api = gogs_client.GogsApi(env.GITEA_API_URL)
        _path = f"/repos/{env.REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}/{pv_file_name}?ref=main"
        _body = {
            "content": b64encode(yaml.encode("utf-8")).decode("utf-8"),
            "message": f"Add {pv_file_name}",
            "branch": "main",  
        }
        content = api.post(path = _path, auth = self.gogs_token, data = _body)
        return loads(content.text)
        
    