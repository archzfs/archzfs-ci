import os
from buildbot.plugins import util

enableGithubLogin = os.environ.get("ENABLE_GITHUB_LOGIN", "false")  == "true"

# authentication using github
if enableGithubLogin:
    githubGroupPrefix = os.environ.get("GITHUB_GROUP_PREFIX", "archzfs/")
    githubGroupRole = os.environ.get("GITHUB_GROUP_ROLE", "Owners")
    githubClientId = os.environ.get("GITHUB_CLIENT_ID", "")
    githubClientSecret = os.environ.get("GITHUB_CLIENT_SECRET", "")

    authz = util.Authz(
        allowRules = [
            util.AnyControlEndpointMatcher(role=githubGroupRole)
        ],
        roleMatchers=[
            util.RolesFromGroups(groupPrefix=githubGroupPrefix)
        ]
    )

    auth = util.GitHubAuth(
        githubClientId,
        githubClientSecret,
        apiVersion=4,
        getTeamsMembership=True
    )
# authentication using an admin user
else:
    adminName = os.environ.get("ADMIN_NAME", "")
    adminPassword = os.environ.get("ADMIN_PASSWORD", "")

    authz = util.Authz(
        allowRules = [
            util.AnyControlEndpointMatcher(role="admin")
        ],
        roleMatchers = [
            util.RolesFromUsername(roles=['admin'], usernames=[adminName])
        ]
    )
    auth = util.UserPasswordAuth({adminName: adminPassword})
