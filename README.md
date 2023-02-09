This is a very barebones example of a GitHub integration. It runs a
flask app that will receive GitHub webhook events. It can be installed
and invoked with:

```
$ poetry install
$ poetry run ghlisten my-cert.pem <my numeric GitHub app id> <port to listen on>
```

See https://python-poetry.org/ for information on installing and using `poetry`.

See https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app
for steps on creating an app and generating the cert.

