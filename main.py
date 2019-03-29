import urllib.request as request
import getopt, sys
import collections
import datetime
import json

baseUrl = "https://api.github.com/users/{0}/events?page={1}&per_page={2}"
accountId = "BLumia"
summaryCount = 30
summaryPage = 1
summaryDict = collections.OrderedDict()


def usage():
	print('''
GitHub User Summary - Get a summary list group by day via GitHub API

Example:
    {0} -a BLumia -c 10

Usage:
    -h          --help            : Display this help
    -a <id>     --account <id>    : GitHub account id
    -c <count>  --count	<count>   : Event count fetched from GitHub (Per page, default: 30, max: 100)
    -p <page>   --page <page>     : N-th page, default is 1
    -o <path>   --output= <path>  : Not implemented...
'''.format(sys.argv[0]))


def main() :
    try :
        opts, _ = getopt.getopt(sys.argv[1:], "a:c:p:ho:e", ["account", "count", "page", "help", "empty", "output="])
    except getopt.GetoptError as err :
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        print("Argument not correct")
        print("Try `{0} -h` to see usage.".format(sys.argv[0]))
        sys.exit(2)

    global baseUrl
    global accountId
    global summaryCount
    global summaryDict

    for o, a in opts:
        if o in ("-u", "--url"):
            baseUrl = a
        elif o in ("-a", "--account"):
            accountId = a
        elif o in ("-c", "--count"):
            if a.isdigit():
                summaryCount = int(a)
            else:
                assert False, "argument not valid"
        elif o in ("-p", "--page"):
            if a.isdigit():
                summaryPage = int(a)
            else:
                assert False, "argument not valid"
        elif o in ("-h", "--help"):
            usage()
            exit()
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-e", "--empty"):
            print("Empty empty empty empty...")
            print("Lazy guy!")
        else:
            assert False, "unhandled option"

    if len(opts) == 0:
        usage()
        exit()

    requestUrl = baseUrl.format(accountId, summaryPage, summaryCount)

    print("Loading summary from GitHub")
    print("Account: `" + accountId + "`")
    if summaryPage != 1 :
        print("Request summary page: " + str(summaryPage))
    print("Request summary count: " + str(summaryCount))

    with request.urlopen(requestUrl) as url :
        rawData = url.read().decode()
        events = json.loads(rawData)
        print("Actual summary count: " + str(len(events)) + '\n')

        for event in events :
            currentEventType = event['type']
            skipCurrentEvent = True
            eventCreateTime = datetime.datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%S%z")
            eventSummaryText = ""
            if currentEventType == 'PullRequestEvent' :
                skipCurrentEvent = False
                pr = event['payload']['pull_request']
                eventSummaryText = "[{0} @ {1}] {2} [{3}]".format("PR", event['repo']['name'], pr['title'], "submitted")
                # print('Event Time: ' + eventCreateTime.strftime("%Y-%m-%d"))
                # print('Repo: ' + event['repo']['name'])
                # print('PR Title: ' + pr['title'])
                # print('PR Url: ' + pr['html_url'])
            elif currentEventType == 'IssuesEvent' :
                skipCurrentEvent = False
                issue = event['payload']['issue']
                eventSummaryText = "[{0} @ {1}] {2} [{3}]".format("Issues", event['repo']['name'], issue['title'], event['payload']['action'])
                # print('Event Time: ' + eventCreateTime.strftime("%Y-%m-%d"))
                # print('Repo: ' + event['repo']['name'])
                # print('Issue Title: ' + issue['title'])
                # print('Issue Action: ' + event['payload']['action'])
            elif currentEventType == 'GollumEvent' :
                skipCurrentEvent = False
                wikiPages = event['payload']['pages']
                wikiPagesSummaryText = ""
                wikiPagesActionText = wikiPages[0]['action']
                if (len(wikiPages) == 1) :
                    wikiPagesSummaryText = wikiPages[0]['title']
                else :
                    wikiPagesSummaryText = "{0} (+{1} more)".format(wikiPages[0]['title'], len(wikiPages))
                eventSummaryText = "[{0} @ {1}] {2} [{3}]".format("Wiki", event['repo']['name'], wikiPagesSummaryText, wikiPagesActionText)

            if skipCurrentEvent :
                print(event['type'] + ' Skipped')
            else :
                summaryDict.setdefault(eventCreateTime.strftime("%Y-%m-%d"), []).append(eventSummaryText)

        print("\n----------- Item Get Border Line -----------\n")

        for when, oneDay in summaryDict.items():
            print(when + ":")
            for commit in oneDay:
                print(" * " + commit)
            print("")


if __name__ == "__main__":
    main()