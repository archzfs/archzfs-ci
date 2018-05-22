import os
from buildbot.plugins import *

githubRepo = os.environ.get("GITHUB_REPO", "archzfs/archzfs")

######## BUILDERS
# The 'builders' list defines the Builders, which tell Buildbot how to perform a build:
# what steps, and which workers can execute them.  Note that any particular build will
# only take place on one worker.

def getBuilders(allWorkers, mainWorkers, kernels, buildLock):

    builders = []

    #
    # generate test+build/kernel builder
    #

    kernelFactory = util.BuildFactory();

    def canStartBuild(builder, wfb, request):
        return request.properties['worker'] is wfb.worker.name

    # run 'build.sh kernel make' to compile packages for a kernel
    kernelFactory.addStep(steps.ShellCommand(
        name=util.Interpolate("build.sh %(prop:kernel)s make"),
        command=util.Interpolate("sudo bash build.sh -d %(prop:kernel)s make"),
        haltOnFailure=True,
        description=util.Interpolate("Compile %(prop:kernel)s packages")))

    builders.append(util.BuilderConfig(
        name="build-test/kernel",
        workernames=allWorkers,
        canStartBuild=canStartBuild,
        workerbuilddir="all",
        factory=kernelFactory))

    #
    # generate build/common builder
    #

    commonFactory = util.BuildFactory();
    # run 'build.sh all update' to generate all PKGBUILDs
    commonFactory.addStep(steps.ShellCommand(
        name="build.sh all update",
        command="sudo bash build.sh -d -u all update",
        haltOnFailure=True,
        description="Generate all PKGBUILDs"))

    # run 'build.sh common make' to compile common packages
    commonFactory.addStep(steps.ShellCommand(
        name="build.sh common make",
        command="sudo bash build.sh -d common make",
        haltOnFailure=True,
        description="Compile common packages"))

    # run 'build.sh common-git make' to compile common-git packages
    commonFactory.addStep(steps.ShellCommand(
        name="build.sh common-git make",
        command="sudo bash build.sh -d common-git make",
        haltOnFailure=True,
        description="Compile common-git packages"))

    # prepare for aarch64
    commonFactory.addStep(steps.ShellCommand(
        name="aarch64: prepare",
        command="sudo makechrootpkg -r /scratch/.chroot64 -l root -I /packages/aarch64-linux-gnu-libutil-linux-*.pkg.tar.xz",
        haltOnFailure=True,
        description="Prepare aarch64"))

    # run 'build.sh common make' to compile common packages for aarch64
    commonFactory.addStep(steps.ShellCommand(
        name="aarch64: build.sh common make",
        command="sudo bash build.sh -d common make -c=/root/makepkg.conf.aarch64",
        haltOnFailure=True,
        description="Compile common packages"))

    # run 'build.sh common-git make' to compile common-git packages for aarch64
    commonFactory.addStep(steps.ShellCommand(
        name="aarch64: build.sh common-git make",
        command="sudo bash build.sh -d common-git make -c=/root/makepkg.conf.aarch64",
        haltOnFailure=True,
        description="Compile common-git packages"))
    
    builders.append(util.BuilderConfig(
        name="build/common",
        workernames=allWorkers,
        canStartBuild=canStartBuild,
        workerbuilddir="all",
        properties={'buildername_report':'build/common'},
        factory=commonFactory))

    #
    # generate test+build builder
    #

    build = util.BuildFactory();

    # fix permissions
    build.addStep(steps.ShellCommand(
        name="fix permissions",
        command="sudo chown -R buildbot:buildbot ."))

    # git update
    build.addStep(steps.Git(
        repourl='git://github.com/' + githubRepo + '.git',
        mode='full',
        method='copy',
        haltOnFailure=True))

    # adjust config file, delete all previous build packages
    build.addStep(steps.ShellCommand(
        name="prepare working directory",
        command="sed -i 's/demizer/buildbot/' conf.sh && sudo ccm64 d || true"))

    # trigger build for common packages
    build.addStep(steps.Trigger(
        name="build/common",
        schedulerNames=['build/common'],
        waitForFinish=True,
        set_properties={
            'worker': util.Property('workername'),
        }))

    # trigger build + test for all kernels
    for idx,kernel in enumerate(kernels):
        build.addStep(steps.Trigger(
            name="build-test/%s" %(kernel),
            schedulerNames=['build-test/kernel'],
            waitForFinish=True,
            set_properties={
                'kernel' : kernel,
                'worker': util.Property('workername'),
                'buildername_report': "build+test/" + kernel,
                'virtual_builder_name': "build-test/%s" %(kernel)
            }))

    builders.append(util.BuilderConfig(
        name="build-test",
        workernames=mainWorkers,
        workerbuilddir="all",
        properties={'buildername_report':'build+test'},
        locks=[buildLock.access('exclusive')],
        factory=build))
    
    return builders
