from pathlib import Path
from github import Github, GithubIntegration


class GHConnect:
    """
    Wrapper for functionality our app needs from the `github` library.
    """

    def __init__(self, app_id: str, cert_path: Path, org: str, repo: str) -> None:
        """
        Apps can be installed on a per-org, per-repo basis. To make API calls we need
        to know our own app ID, our private cert, and the org and repo for the installed
        app. API calls made on behalf of the app are rate-limited per install.
        """
        self.app_id = app_id
        self.app_key = self.cert_from_path(cert_path)
        self.github_integration = self.get_integration()
        self.org = org
        self.repo = repo

    def cert_from_path(self, cert_path: Path) -> str:
        """
        Helper to read the cert file, for use in in the jwt.
        """
        with open(cert_path, "r") as cert:
            key = cert.read()
            return key

    def get_integration(self) -> GithubIntegration:
        """
        The `GithubIntegration` instance we use for our connection.
        See https://docs.github.com/en/developers/apps/building-github-apps/authenticating-with-github-apps#generating-a-json-web-token-jwt
        """
        return GithubIntegration(
            self.app_id,
            self.app_key,
        )

    def create_conn(self) -> Github:
        """
        Putting it all together, this gets the necessary info to make calls on
        behalf of a particular installation of our app.
        """
        app_install = self.github_integration.get_installation(self.org, self.repo).id
        token = self.github_integration.get_access_token(app_install).token
        return Github(login_or_token=token)

    def get_repo_list(self, user: str) -> list[str]:
        """
        Basic example showing information we can get. In `main.py` it's used to get
        a new repo list after receiving a webhook event, but it could be invoked
        any time.
        """
        gh = self.create_conn()
        gh.get_user(user).get_repos()
        return [str(r) for r in gh.get_user(user).get_repos()]
