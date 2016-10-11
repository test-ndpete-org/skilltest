#Nate Peterson
#Skill test October 2016

from sys import argv
from github import Github

def main():
    # Sanity Check
    #Check for token as an argument fail if not provided
    if not len(argv)>2:
        print("Missing github token or organization")
        print("Usage: python pyGit.py [token] [org]")
        exit(1)

    g = Github(login_or_token=argv[1])

    for u in g.get_organization(argv[2]).get_members():
        if not u.name:
            print("FAILED:login: %s name: %s email: %s" % (u.login,u.name,u.email))
        else:
            print("PASSED:login: %s name: %s email: %s" % (u.login,u.name,u.email))


if __name__ == '__main__':
    main()
