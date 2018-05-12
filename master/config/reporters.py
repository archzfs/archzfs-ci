import os
import buildbot.plugins

enableGithubStatus = os.environ.get("ENABLE_GITHUB_STATUS_REPORT", "false")  == "true"
enableDeploy = os.environ.get("ENABLE_DEPLOY", "false")  == "true"
enableEmail = os.environ.get("ENABLE_DEPLOY_NOTIFICATIONS", "false")  == "true"

####### BUILDBOT REPORTERS

def getReporters(reportSchedulerNames, reportBuilderNames):
    reporters = []

    # github status reporter
    if enableGithubStatus:
        context = buildbot.plugins.util.Interpolate("bb/%(prop:buildername_report)s")
        gs = buildbot.plugins.reporters.GitHubStatusPush(
            token=os.environ.get("GITHUB_TOKEN", ""),
            context=context,
            startDescription='Build started.',
            endDescription='Build done.')
        reporters.append(gs)

    # email notifications
    if enableDeploy and enableEmail:
        emailFrom = os.environ.get("EMAIL_FROM", "noreply@example.com")
        recipients = os.environ.get("NOTIFY_RECIPIENTS", "").split('|')
        smtpServer = os.environ.get("SMTP_SERVER", "")
        smtpPort = int(os.environ.get("SMTP_PORT", "587"))
        smtpUser = os.environ.get("SMTP_USER", "")
        smtpTls = os.environ.get("SMTP_TLS", "false")  == "true"
        smtpPassword = os.environ.get("SMTP_PASSWORD", "")

        mn = buildbot.plugins.reporters.MailNotifier(
            mode=('failing', 'warnings', 'exception'),
            builders=reportBuilderNames,
            schedulers=reportSchedulerNames,
            fromaddr=emailFrom,
            sendToInterestedUsers=False,
            extraRecipients=recipients,
            relayhost=smtpServer, smtpPort=smtpPort, useTls=smtpTls,
            smtpUser=smtpUser,
            smtpPassword=smtpPassword)
        reporters.append(mn)
        
    return reporters
