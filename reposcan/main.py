import argparse

from flask import Flask, request
from .gitwrapper import GHConnect


app = Flask("pybot")


@app.route("/", methods=["POST"])
def bot():
    """
    This view gets webhooks from GitHub:
    https://docs.github.com/en/developers/webhooks-and-events/webhooks/about-webhooks
    """
    # Get the event payload
    payload = request.json
    gh = GHConnect(
        app_id=app.config["app_id"],
        cert_path=app.config["cert"],
        org=payload["repository"]["owner"]["login"],
        repo=payload["repository"]["name"],
    )

    # advanced logging mechanism to send data to stdout
    print(payload)

    current_repos = gh.get_repo_list()
    for repo in current_repos:
        print(repo)

    return "ok"


def cli_parser() -> argparse.Namespace:
    """
    Basic parser so we can invoke our server with:

        $ ghlisten my-cert.pem <my numeric GitHub app id> <port to listen on>
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("cert")
    parser.add_argument("appid")
    parser.add_argument("port")
    return parser.parse_args()


def main() -> None:
    """
    In `pyproject.toml` a script named `ghlisten` will invoke this function.
    This gathers up the cli args and launches the flask app.
    """
    args = cli_parser()
    app.config["cert"] = args.cert
    app.config["app_id"] = args.appid
    app.config["port"] = args.port
    app.run(debug=False, port=app.config["port"])
