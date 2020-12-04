import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import csv

thread_index = []
author = []
text = []
likes = []
publishInfo = []
repliesNum = []

def get_bound(len_a, len_t, len_l, len_p, len_r):
	bound = len_a
	if bound > len_t:
		bound = len_t
	if bound > len_l:
		bound = len_l
	if bound > len_p:
		bound = len_p
	if bound > len_r:
		bound = len_r
	return bound

def load_all_replies():
	replies_left_to_load = 0
	for replies_bundle in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#replies"))):
		num_of_tries = 2
		need_to_see_comments = 1

		while(need_to_see_comments == 1):
			try:
				view_replies = replies_bundle.find_element_by_id("more-replies")
				view_replies.click()	
				replies_left_to_load = 1
				need_to_see_comments = 0
			except:
				if (num_of_tries > 0):
					num_of_tries -= 1
					time.sleep(5)
				else:
					need_to_see_comments = 0
		num_of_tries = 3

		while(replies_left_to_load == 1):
			try:
				more_replies = replies_bundle.find_element_by_tag_name('yt-next-continuation')
				more_replies.click()
				time.sleep(5)
			except:
				#print('We are in the except statement')
				if (num_of_tries > 0):
					num_of_tries -= 1
					time.sleep(5)
				else:
					replies_left_to_load = 0
					#print('We reached the end of the comment thread for the current parent thread')

with Chrome(executable_path="/Users/hildamendoza/Downloads/chromedriver.exe") as driver:
	wait = WebDriverWait(driver,15)
	driver.get("https://www.youtube.com/watch?v=dmDbesougG0")


	for item in range(80):	#(150):	#200): 
		wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
		time.sleep(15)


	load_all_replies()	# load all of the replies for the parent comments
	time.sleep(15)

	load_comments = 1
	
	while (load_comments == 1):
		try:
			loaded_comments = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-comment-thread-renderer')))	#driver.find_elements_by_tag_name('ytd-comment-thread-renderer')
			load_comments = 0
		except:
			time.sleep(5)
	
	main_comment_index = 0	

	# get the chucks of information for every parent comment
	for replies_bundle in loaded_comments:		#wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-comment-thread-renderer'))):
		main_comment_index += 1	
		thread_index.append(main_comment_index)
		
		curr_author_and_publish = replies_bundle.find_element_by_id("header-author").text
		next_line_index = curr_author_and_publish.find("\n")
		
		if (next_line_index > -1):
			authorName = curr_author_and_publish[:next_line_index]
			publishDate = curr_author_and_publish[(next_line_index + 1):]
 
			author.append(authorName)	# author_name
			publishInfo.append(publishDate)	# publishInfo
		else:
			print('NextLine was not found! -> author and publishDate Error!')
			
			author.append('Error: Not Found')	# author_name
			publishInfo.append('Error: Not Found')	# publishInfo
		
		
		curr_like_num = replies_bundle.find_element_by_id("vote-count-middle").text		
		if (curr_like_num == ''):
			curr_like_num = '0'
		likes.append(curr_like_num)		# num_of_likes


		comment_text = replies_bundle.find_element_by_id("content-text").text
		text.append(comment_text)		# comment_text

		replies_num = replies_bundle.find_element_by_id("replies").text
							# replies_num
		if (replies_num == ""):
			repliesNum.append(0)
		else:	
			view_text = "View "
			repNum = replies_num[5:]
			if (repNum[0] == 'r'):
				repliesNum.append(1)
			else:
				end_of_repNum = repNum.find(" ")
				if (end_of_repNum > -1):
					num_of_replies = repNum[:end_of_repNum]
					repliesNum.append(num_of_replies)
				else:
					repliesNum.append('Error: no space found between number and \"replies\"')


		comment_replies = replies_bundle.find_elements_by_tag_name('ytd-comment-renderer')
		i = -1
		for curr_reply in comment_replies:	
			i += 1	
			if (i > 0):
				
				thread_index.append(main_comment_index)
			
				curr_author_and_publish = curr_reply.find_element_by_id("header-author").text
				next_line_index = curr_author_and_publish.find("\n")
		
				if (next_line_index > -1):
					authorName = curr_author_and_publish[:next_line_index]
					publishDate = curr_author_and_publish[(next_line_index + 1):]
 
					author.append( authorName)	# author_name
					publishInfo.append(publishDate)	# publishInfo
				else:
					print('NextLine was not found! -> author and publishDate Error!')
			
					author.append('Error: Not Found')	# author_name
					publishInfo.append('Error: Not Found')	# publishInfo

				curr_like_num = curr_reply.find_element_by_id("vote-count-middle").text		
				if (curr_like_num == ''):
					curr_like_num = '0'
				likes.append(curr_like_num)		# num_of_likes



				comment_text = curr_reply.find_element_by_id("content-text").text
				text.append(comment_text)		# comment_text
	
				try:
					replies_num = curr_reply.find_element_by_id("replies").text
									# replies_num
					if (replies_num == ""):
						repliesNum.append(0)
					else:	
						view_text = "View "
						repNum = replies_num[5:]
						if (repNum[0] == 'r'):
							repliesNum.append(1)
						else:
							end_of_repNum = repNum.find(" ")
							if (end_of_repNum > -1):
								num_of_replies = repNum[:end_of_repNum]
								repliesNum.append(num_of_replies)
							else:
								repliesNum.append('Error: no space found between number and \"replies\"')

				except:
					repliesNum.append(0)

with open('comments.csv', 'w', newline='') as comments_file:
	fieldnames = ['Comment Thread #', 'Author Name', 'Comment Text', 'Like Count', 'Published Date', 'Total Reply Count']
	comments_writer = csv.DictWriter(comments_file, fieldnames=fieldnames)
	comments_writer.writeheader()

	bound = get_bound(len(author), len(text), len(likes), len(publishInfo), len(repliesNum))		
	i = 0
	
	print('Bound: ', bound, '| \nLenghts:')
	print('Authors: ', len(author),'| Text: ', len(text),'| Likes: ', len(likes),'| PublishInfo: ', len(publishInfo), '| RepliesNum: ', len(repliesNum))
	
	while i < bound:
		comments_writer.writerow({'Comment Thread #' : thread_index[i], 'Author Name' : author[i], 'Comment Text': text[i], 'Like Count': likes[i], 'Published Date': publishInfo[i], 'Total Reply Count': repliesNum[i]})

		i += 1

print('We\'re done getting all of the comment texts!')
