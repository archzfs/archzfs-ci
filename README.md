# archzfs-ci

Continuous integration for the archzfs packages using buildbot.

## Dependencies
- docker
- docker-compose

## Running
- Clone this repository:
```
git clone https://github.com/minextu/archzfs-ci
```
- Build the docker images
```
./build.sh
```
- Start the web interface
```
docker-compose up
```

Buildbot will run under `localhost:8080` after that. The default admin user is admin with an empty password.

### Trigger a manual build
Login as admin and select a builder (Builds -> Builders). Press the force button and leave all fields empty to just build the master branch.

## Configuration
The main configuration is located in `conf.env`.

### GitHub Integration
You will need to generate a new access token [here](https://github.com/settings/tokens).
Tick the `repo:status` and `repo_deployment` permissions.
Copy the resulting token into `conf.env` (`GITHUB_TOKEN=`).

Next you will need to create a webhook, to notify buildbot about new commits or pull requests:
Visit the archzfs repo settings (of your fork), choose `Webhooks` and add a new one.

- Playload url: located at `http://<your-public-archzfs-ci-url>/change_hook/github`
- Content type: `application/x-www-form-urlencoded`
- Secret: Password used to authenticate github requests
- Events: Tick `Push` and `Pull requests`

Enter your secret and the name of your archzfs fork in `conf.env` (`GITHUB_HOOK_SECRET=`, `GITHUB_REPO=`).

Just restart after that (`docker-compose restart`) and you're done.
