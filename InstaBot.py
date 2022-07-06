from matplotlib.style import use
import requests, urllib  #Importing "requests" Libabry and "urllib" 
from textblob import TextBlob  #Simple Text Processing library 
from textblob.sentiments import NaiveBayesAnalyzer  #For Negetive Comments


#APP_ACCESS_TOKEN = ''    #Sir 
APP_ACCESS_TOKEN = '<api-token>'    #Me


BASE_URL = 'https://api.instagram.com/v1/'   #Assigning Base URL to a veriable for further use


#Function declaration to get your own info


#Defining a Function for getting our own information
def self_info():
    request_url = BASE_URL + f'users/self/?access_token={APP_ACCESS_TOKEN}' 
    print(f'GET request url : {request_url}')
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200: #If Data is received
        if len(user_info['data']): #If the received Data is not Blank
            print(f"Username: {user_info['data']['username']}") 
            print(f"No. of followers: {user_info['data']['counts']['followed_by']}")
            print(f'No. of people you are following: %s' % (user_info['data']['counts']['follows']))
            print(f'No. of posts: %s' % (user_info['data']['counts']['media']))
        else:
            print('User does not exist!')
    else:
        print('Status code other than 200 received!')



#Function declaration to get the ID of a user by username


def get_user_id(insta_username):
    request_url = BASE_URL + f'users/search?q={insta_username}&access_token={APP_ACCESS_TOKEN}'
    print(f'GET request url : {request_url}')
    user_info = requests.get(request_url).json() #Getting all of the User Information

    if user_info['meta']['code'] == 200: #If The User info is received
        if len(user_info['data']): #If the received Data is not Blank
            return user_info['data'][0]['id'] #Printing The User ID of the User from the received User Info
        else:
            return None
    else:
        print('Status code other than 200 received!')
        exit()



#Function declaration to get the info of a user by username

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print('User does not exist!')
        exit()
    request_url = BASE_URL + f'users/{user_id}?access_token={APP_ACCESS_TOKEN}'
    print(f'GET request url : {request_url}')
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200: #If The User info is received
        if len(user_info['data']): #If the received Data is not Blank
            print(f"Username: {user_info['data']['username']}")
            print(f"No. of followers: {user_info['data']['counts']['followed_by']}")
            print(f"No. of people you are following: {user_info['data']['counts']['follows']}")
            print(f"No. of posts: {user_info['data']['counts']['media']}")
        else:
            print('There is no data for this user!')
    else:
        print('Status code other than 200 received!')



#Function declaration to get your recent post



def get_own_post():
    request_url = BASE_URL + f'users/self/media/recent/?access_token={APP_ACCESS_TOKEN}'
    print(f'GET request url : {request_url}')
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print('Your image has been downloaded!')
        else:
            print('Post does not exist!')
    else:
        print('Status code other than 200 received!')



#Function declaration to get the recent post of a user by username

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None: #If No user Id Was Given
        print('User does not exist!')
        exit()
    request_url = BASE_URL + f'users/{user_id}/media/recent/?access_token={APP_ACCESS_TOKEN}'
    print(f'GET request url : {request_url}')
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200: #If The the Post is received
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print('Your image has been downloaded!')
        else:
            print('Post does not exist!')
    else:
        print('Status code other than 200 received!')


		
#Function declaration to get the ID of the recent post of a user by username

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print('User does not exist!')
        exit()
    request_url = BASE_URL + f'users/{user_id}/media/recent/?access_token={APP_ACCESS_TOKEN}'
    print(f'GET request url : {request_url}')
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:  #If The the PostID is received
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print('There is no recent post of the user!')
            exit()
    else:
        print('Status code other than 200 received!')
        exit()




#Function declaration to like the recent post of a user

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = BASE_URL + f'media/{media_id}/likes'
    payload = {"access_token": APP_ACCESS_TOKEN}
    print(f'POST request url : {request_url}')
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200: #If No error Occurs and The Like is Done
        print('Like was successful!')
    else:
        print('Your like was unsuccessful. Try again!')



#Function declaration to make a comment on the recent post of the user

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = BASE_URL + f'media/{media_id}/comments'
    print(f'POST request url : {request_url}')

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print("Successfully added a new comment!")
    else:
        print("Unable to add comment. Try again!")


		
		
#Function declaration to make delete negative comments from the recent post

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = BASE_URL + f'media/{media_id}/comments/?access_token={APP_ACCESS_TOKEN}'
    print(f'GET request url : {request_url}')
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Simple Implimentation Of Deleting Negetive Comments
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print(f'Negative comment : {comment_text}')
                    delete_url = BASE_URL + f'media/{media_id}/comments/{comment_id}/?access_token={APP_ACCESS_TOKEN}'
                    print(f'DELETE request url : {delete_url}')
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print('Comment successfully deleted!\n')
                    else:
                        print('Unable to delete comment!')
                else:
                    print(f'Positive comment : {comment_text}\n')
        else:
            print('There are no existing comments on the post!')
    else:
        print('Status code other than 200 received!')





#Function To Start The Bot
def start_bot():
    while True:
        print('\n')
        print('Hey! Welcome to instaBot!')
        print('Here are your menu options:')
        print("a.Get your own details\n")
        print("b.Get details of a user by username\n")
        print("c.Get your own recent post\n")
        print("d.Get the recent post of a user by username\n")
        print("e.Get a list of people who have liked the recent post of a user\n")
        print("f.Like the recent post of a user\n")
        print("g.Get a list of comments on the recent post of a user\n")
        print("h.Make a comment on the recent post of a user\n")
        print("i.Delete negative comments from the recent post of a user\n")
        print("j.Exit")

		#Get Users Choice 
        choice = input("Enter you choice: ")
		
		#Processing The Choice to call the appropriate function
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="e":
           insta_username = input("Enter the username of the user: ")
           get_like_list(insta_username)
        elif choice=="f":
           insta_username = input("Enter the username of the user: ")
           like_a_post(insta_username)
        elif choice=="g":
           insta_username = input("Enter the username of the user: ")
           get_comment_list(insta_username)
        elif choice=="h":
           insta_username = input("Enter the username of the user: ")
           post_a_comment(insta_username)
        elif choice=="i":
           insta_username = input("Enter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice == "j":
            exit()
        else:
            print("wrong choice")

start_bot() #Calling the start_bot() function again to print the menu every time the program ends.
