import os
from buildbot.plugins import *

enableAurPush = os.environ.get("ENABLE_AUR_PUSH", "false")  == "true"
enableArchiso = os.environ.get("ENABLE_ARCHISO", "false")  == "true"

def getDeployBuilders(kernels, buildLock):

    deployBuilders = []

    #
    # generate the deploy builder
    #

    deploy = util.BuildFactory()

    # add packages to repo
    deploy.addStep(steps.ShellCommand(
        name="repo.sh all azfs",
        command="bash repo.sh -d all azfs",
        haltOnFailure=True,
        description="Add packages to repo"))

    # push packages to remote repo
    deploy.addStep(steps.ShellCommand(
        name="push.sh -r",
        command="bash push.sh -r -d",
        haltOnFailure=True,
        description="Push packages to remote repo"))

    # push packages to the aur
    if enableAurPush:
        deploy.addStep(steps.ShellCommand(
            name="push.sh -p all",
            command="bash push.sh -p -d all",
            haltOnFailure=True,
            description="Push packages to the AUR"))

    deployBuilders.append(util.BuilderConfig(
        name="deploy",
        workernames="archzfs-deploy",
        workerbuilddir="all",
        properties={'buildername_report':'deploy'},
        factory=deploy))

    #
    # generate the test+build+deploy builder
    #

    deploy = util.BuildFactory()

    # fix permissions
    deploy.addStep(steps.ShellCommand(
        name="fix permissions",
        command="sudo chown -R buildbot:buildbot ."))

    # git update
    deploy.addStep(steps.Git(
        repourl='git://github.com/' + os.environ.get("GITHUB_REPO", "archzfs/archzfs") + '.git',
        mode='incremental',
        haltOnFailure=True))

    # prepare workdir
    remoteServer = os.environ.get("REMOTE_REPO_SERVER", "")
    remotePath = os.environ.get("REMOTE_REPO_PATH", "")
    remoteRepoBasename = os.environ.get("REMOTE_REPO_BASENAME", "")
    deploy.addStep(steps.ShellCommand(
        name="prepare workdir",
        haltOnFailure=True,
        command="bash /worker/prepare-workdir.sh '%s' '%s' '%s' '%s'\
                " %(remoteServer, remotePath, remoteRepoBasename, os.environ.get("ENABLE_AUR_PUSH", "false"))))

    # trigger build for common packages
    deploy.addStep(steps.Trigger(
        name="build/common",
        schedulerNames=['build/common'],
        waitForFinish=True,
        haltOnFailure=True,
        set_properties={
            'worker': util.Property('workername'),
        }))

    # trigger build + test for all kernels
    for idx,kernel in enumerate(kernels):
        deploy.addStep(steps.Trigger(
            name="build-test/%s" %(kernel),
            schedulerNames=['build-test/kernel'],
            waitForFinish=True,
            haltOnFailure=True,
            set_properties={
                'kernel' : kernel,
                'worker': util.Property('workername'),
                'buildername_report': "build+test/" + kernel,
                'virtual_builder_name': "build-test/%s" %(kernel)
            }))

    # trigger deploy builder
    deploy.addStep(steps.Trigger(
        name="deploy",
        schedulerNames=['deploy'],
        waitForFinish=True,
        haltOnFailure=True))

    deployBuilders.append(
        util.BuilderConfig(name="build-test-deploy",
                            workernames="archzfs-deploy",
                            workerbuilddir="all",
                            properties={'buildername_report':'build+test+deploy'},
                            locks=[buildLock.access('exclusive')],
                            factory=deploy))

    #
    # generate the archiso builder
    #
    
    if enableArchiso:
        archiso = util.BuildFactory()

        # fix permissions
        archiso.addStep(steps.ShellCommand(
            name="fix permissions",
            command="sudo chown -R buildbot:buildbot ."))

        # git update
        archiso.addStep(steps.Git(
            repourl='git://github.com/' + os.environ.get("GITHUB_REPO", "archzfs/archzfs") + '.git',
            mode='incremental',
            haltOnFailure=True))

        # prepare workdir
        remoteServer = os.environ.get("REMOTE_REPO_SERVER", "")
        remotePath = os.environ.get("REMOTE_REPO_PATH", "")
        remoteRepoBasename = os.environ.get("REMOTE_REPO_BASENAME", "")
        archiso.addStep(steps.ShellCommand(
            name="prepare workdir",
            haltOnFailure=True,
            command="bash /worker/prepare-workdir.sh '%s' '%s' '%s' '%s'\
                    " %(remoteServer, remotePath, remoteRepoBasename, os.environ.get("ENABLE_AUR_PUSH", "false"))))

        # build the non git archlinux zfs iso
        archiso.addStep(steps.ShellCommand(
            name="archiso/build.sh",
            command="sudo bash archiso/build.sh -v",
            haltOnFailure=True,
            description="Embed zfs into archiso"))

        # build the git archlinux zfs iso
        archiso.addStep(steps.ShellCommand(
            name="archiso/build.sh -g",
            command="sudo bash archiso/build.sh -vg",
            haltOnFailure=True,
            description="Embed zfs-git into archiso"))
        
        # push isos to remote repo
        archiso.addStep(steps.ShellCommand(
            name="archiso/push.sh -i",
            command="bash push.sh -i -d",
            haltOnFailure=True,
            description="Push iso's to remote repo"))

        deployBuilders.append(
            util.BuilderConfig(name="archiso",
                                workernames="archzfs-deploy",
                                workerbuilddir="all",
                                properties={'buildername_report':'archiso'},
                                locks=[buildLock.access('exclusive')],
                                factory=archiso))

    return deployBuilders
