import os
import buildbot.plugins
enableDeploy = os.environ.get("ENABLE_DEPLOY", "false")  == "true"
enableArchiso = os.environ.get("ENABLE_ARCHISO", "false")  == "true"

####### SCHEDULERS
# Configure the Schedulers, which decide how to react to incoming changes

schedulers = []
reportSchedulerNames = []

# build and test all packages if changes accour
# in any branch or in a pull request
# ignore master branch if deploy is enabled

#if enableDeploy:
#    changeFilter = buildbot.plugins.util.ChangeFilter(branch_re='(?!master)');
#else:
#    changeFilter = None
#schedulers.append(buildbot.plugins.schedulers.AnyBranchScheduler(
#    name="github any branch",
#    treeStableTimer=10,
#    change_filter=changeFilter,
#    builderNames= ["build-test"]))

# add force button in user interface
schedulers.append(buildbot.plugins.schedulers.ForceScheduler(
    name="force",
    builderNames=["build-test"]))

# add common builder
schedulers.append(buildbot.plugins.schedulers.Triggerable(
    name="build/common",
    builderNames=["build/common"]))

# add kernel builder
schedulers.append(buildbot.plugins.schedulers.Triggerable(
    name="build-test/kernel",
    builderNames=["build-test/kernel"]))

# deploy schedulers
if enableDeploy:
    # add deploy testing builder
    schedulers.append(buildbot.plugins.schedulers.Triggerable(
        name="deploy-to-testing",
        builderNames=['deploy-to-testing']))

    # force deploy testing button
    schedulers.append(buildbot.plugins.schedulers.ForceScheduler(
        name="force-deploy-to-testing",
        buttonName="force deploy to testing",
        builderNames=['build-test-deploy-to-testing']))

    #  deploy stable button
    schedulers.append(buildbot.plugins.schedulers.ForceScheduler(
        name="force-deploy-to-stable",
        buttonName="deploy to stable",
        builderNames=['deploy-to-stable']))

    # deploy when changes to master occour
    schedulers.append(buildbot.plugins.schedulers.SingleBranchScheduler(
        name="github master deploy",
        change_filter=buildbot.plugins.util.ChangeFilter(branch='master'),
        treeStableTimer=10,
        builderNames=['build-test-deploy-to-testing']))

    # deploy once a day
    schedulers.append(buildbot.plugins.schedulers.Nightly(
        name='daily deploy',
        change_filter=buildbot.plugins.util.ChangeFilter(branch='master'),
        builderNames=['build-test-deploy-to-testing'],
        hour=3, minute=0))

    reportSchedulerNames = ['force-deploy-to-testing', 'force-deploy-to-stable', 'github master deploy', 'daily deploy']

# archiso schedulers
if enableArchiso and enableDeploy:
    # force deploy iso button
    schedulers.append(buildbot.plugins.schedulers.ForceScheduler(
        name="force-iso-deploy",
        buttonName="force iso deploy",
        builderNames=['archiso']))

    # generate iso's once a month
    schedulers.append(buildbot.plugins.schedulers.Nightly(
        name='monthly archiso',
        change_filter=buildbot.plugins.util.ChangeFilter(branch='master'),
        builderNames=['archiso'],
        dayOfMonth=1, hour=6, minute=0))

    reportSchedulerNames.append('force-iso-deploy')
    reportSchedulerNames.append('monthly archiso')
