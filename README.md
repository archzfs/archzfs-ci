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
docker-compose build
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
#### Status report
You will need to generate a new access token [here](https://github.com/settings/tokens).
Tick the `repo:status` and `repo_deployment` permissions.
Copy the resulting token into `conf.env` (`GITHUB_TOKEN=`).

Next you will need to create a webhook, to notify buildbot about new commits or pull requests:
Visit the archzfs repo settings (of your fork), choose `Webhooks` and add a new one.

- Payload url: located at `http://<your-public-archzfs-ci-url>/change_hook/github`
- Content type: `application/x-www-form-urlencoded`
- Secret: Password used to authenticate github requests
- Events: Tick `Push` and `Pull requests`

Set `ENABLE_GITHUB_STATUS_REPORT` to `true` and enter your secret and the name of your archzfs fork in `conf.env` (`GITHUB_HOOK_SECRET=`, `GITHUB_REPO=`).

Just restart after that (`docker-compose restart`) and you're done.

### Login through GitHub
...

## Automated Deployment
When enabled, packages will get uploaded to a repository after building and testing. This is done on a daily basis or if new commits are pushed to the master branch.

### Setup
You will need to have a webserver with `ssh` and `rsync` installed to host the repository.

1. Create the repo folders on the repo server: a repo folder, a testing repo suffixed with `tesing` and two archive folders using the previous names prefixed with `archive_` (e.g. `/var/www/archzfs`  `/var/www/archzfs-testing`, `/var/www/archive_archzfs` and `/var/www/archive_archzfs-testing`). Grant access to a user, that will be used to update the repo.

2. Generate a new ssh key with no passphrase and save it in `deploy/secrets/ssh_key(.pub)`.

```
ssh-keygen -f deploy/secrets/ssh_key
```

3. Add the newly generated public key to `~/.ssh/.authorized_keys` as user on your repo server.

4. Save the public server keys to `deploy/secrets/ssh_server_hostkeys`.

```
ssh-keyscan archzfs-repo.example.com > deploy/secrets/ssh_server_hostkeys
```

5. Generate a gpg (sub)key to sign the packages and save it to `deploy/secrets/gpg_key`.

```
gpg --gen-key

# copy the gpg key id you'd like to use
gpg --list-secret-keys --keyid-format LONG

# replace <gpg-key-id> with your key id
gpg --armor --export-secret-keys <gpg-key-id> > deploy/secrets/gpg_key
```

6. Open `conf.env` and fill out the options like this:

```
# push built packages to remote repo
ENABLE_DEPLOY=true
REMOTE_REPO_SERVER=user@archzfs-repo.example.com
REMOTE_REPO_PATH=/var/www
REMOTE_REPO_BASENAME=archzfs
GPG_PASSPHRASE=password
```

This would create/update the repository located in `/var/www/archzfs` on the server `archzfs-repo@example.com` using the user `user`.

7. Finally rebuild the docker container (`docker-compose build`) and start buildbot (`docker-compose up`)

### E-Mail notifications
When enabled you'll receive an email when deployment has failed.

Set `ENABLE_DEPLOY_NOTIFICATIONS` to `true` and specify `EMAIL_FROM` `NOTIFY_RECIPIENTS`.
You can have more than one recipient by separating the emails using a `|`.

Fill out all following options according to your E-Mail server.
