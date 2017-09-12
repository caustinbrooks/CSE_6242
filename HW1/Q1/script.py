import csv
import json
import time
import tweepy


# You must use Python 2.7.x
# Rate limit chart for Twitter REST API - https://dev.twitter.com/rest/public/rate-limits

def loadKeys(key_file_name):
    # TODO: put your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>

    # Load keys here and replace the empty strings in the return statement with those keys
    with open(key_file_name) as key_file:
        data = json.load(key_file)

    return data["api_key"], data["api_secret"], data["token"], data["token_secret"]

# Q1.b.(i) - 5 points
def getPrimaryFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' primary friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    primary_friends = []
    # Add code here to populate primary_friends
    if not api.rate_limit_status()['resources']['friends']['/friends/list']['remaining']:
            time.sleep(15*60)
    some_friends = tweepy.Cursor(api.friends,id=root_user).items(no_of_friends)

    users = []
    for id in some_friends:
        users.append(id)

    for friend in users:
        primary_friends.append((root_user,friend.screen_name))

    return primary_friends

# Q1.b.(ii) - 7 points
def getNextLevelFriends(api, friends_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each entry in friends_list
    # rtype: list containing entries in the form of a tuple (friends_list[i], friend)
    next_level_friends = []
    # Add code here to populate next_level_friends
    for name in enumerate(friends_list, start=1):

        some_friends = tweepy.Cursor(api.friends,id=name[1]).items(no_of_friends)
        print("Next level friends pulled for primary friend number " + str(name[0]) + " of " + str(len(friends_list)))
        print("Sleeping for 60 seconds!")
        time.sleep(60)
        users = []
        for id in some_friends:
            users.append(id)

        for friend in users:
            next_level_friends.append((name[1],friend.screen_name))
            #print(name,friend.screen_name)

    return next_level_friends
    #pass
# Q1.b.(iii) - 7 points
def getNextLevelFollowers(api, followers_list, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers for each entry in followers_list
    # rtype: list containing entries in the form of a tuple (follower, followers_list[i])
    next_level_followers = []
    # Add code here to populate next_level_followers
    for name in enumerate(followers_list, start=1):

        some_followers = tweepy.Cursor(api.followers,id=name[1]).items(no_of_followers)
        print("Next level followers pulled for primary friend number " + str(name[0]) + " of " + str(len(followers_list)))
        print("Sleeping for 60 seconds!")
        time.sleep(60)
        users = []
        for id in some_followers:
            users.append(id)

        for follower in users:
            next_level_followers.append((name[1],follower.screen_name))
            #print(name,friend.screen_name)

        pass
    return next_level_followers
    #pass
# Q1.b.(i),(ii),(iii) - 4 points
def GatherAllEdges(api, root_user, no_of_neighbours):
    # TODO:  implement this method for calling the methods getPrimaryFriends, getNextLevelFriends
    #        and getNextLevelFollowers. Use no_of_neighbours to specify the no_of_friends/no_of_followers parameter.
    #        NOT using the no_of_neighbours parameter may cause the autograder to FAIL.
    #        Accumulate the return values from all these methods.
    # rtype: list containing entries in the form of a tuple (Source, Target). Refer to the "Note(s)" in the
    #        Question doc to know what Source node and Target node of an edge is in the case of Followers and Friends.
    all_edges = []
    next_level_root_list = []
    #Add code here to populate all_edges
    primary_friends = getPrimaryFriends(api,root_user,no_of_neighbours)

    prim_friends_obj = api.lookup_users(screen_names=[primary_friends[i][1] for i in xrange(0,len(primary_friends))])


    prim_friends_protection = {primary_friends[i][1]:prim_friends_obj[i].protected for i in xrange(0,len(primary_friends))}

    for prim_friend in prim_friends_protection.keys():

        if not prim_friends_protection[prim_friend]:
            next_level_root_list.append(prim_friend)
        # else:
        #     print(primary_friend_tuple[1].screen_name , "is protected")
        #

    next_level_friends = getNextLevelFriends(api,next_level_root_list,no_of_neighbours)
    next_level_followers = getNextLevelFollowers(api, next_level_root_list,no_of_neighbours)


    all_edges = primary_friends + next_level_friends + next_level_followers

    print(all_edges)

    return all_edges


# Q1.b.(i),(ii),(iii) - 5 Marks
def writeToFile(data, output_file):
    # write data to output_file
    # rtype: None
    f = open(output_file, 'w')

    strData = [str(line[0]) +","+str(line[1])+"\n" for line in data]

    f.writelines(strData)
    f.close()
    pass




"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""

def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_GRAPH = 'graph.csv'
    NO_OF_NEIGHBOURS = 20
    ROOT_USER = 'PoloChau'

    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    edges = GatherAllEdges(api, ROOT_USER, NO_OF_NEIGHBOURS)

    writeToFile(edges, OUTPUT_FILE_GRAPH)


if __name__ == '__main__':
    testSubmission()

