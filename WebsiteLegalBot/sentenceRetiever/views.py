from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import re
from word2number import w2n




def convertWordToNumber(a_TestString):
	l_resultString = ""

	for word in a_TestString.split():
		if word[0] == "o" or word[0] == "t" or word[0] == "f" or word[0] == "s" or word[0] == "e" or word[0] == "n" or word[0] == "t":
			try:
				l_resultString = l_resultString + str(w2n.word_to_num(word))
			except ValueError:
				l_resultString = l_resultString + word
		else:
			l_resultString = l_resultString + word
	return l_resultString



def searchDuration(a_TestString, a_SentenceTypeMatch):
	l_stringEndOfSentenceType = a_TestString[a_SentenceTypeMatch.end():len(a_TestString)]
	l_connecterMatch = re.match('(foraperiodof|forperiodof|period(of)?|for|of|-|)', l_stringEndOfSentenceType)
	
	if l_connecterMatch:

		l_stringEndOfConnecter = l_stringEndOfSentenceType[l_connecterMatch.end():len(l_stringEndOfSentenceType)]	
		l_numberMatch = re.match('([0-9]+[.?][0-9]+)|([0-9]+)', l_stringEndOfConnecter)
		
		if l_numberMatch:
		
			l_stringEndOfNumber = l_stringEndOfConnecter[l_numberMatch.end():len(l_stringEndOfConnecter)]
			l_timeUnitMatch = re.match('(days?|months?|years?)', l_stringEndOfNumber)

			if l_timeUnitMatch:
				# uncomment to undo error report
				return str(a_SentenceTypeMatch.group()) + str(l_numberMatch.group()) + str(l_timeUnitMatch.group())
				print("Found: ", a_SentenceTypeMatch.group(), l_numberMatch.group(), l_timeUnitMatch.group(),)
				# print("\n")
				# print("NO ERROR")
				if l_timeUnitMatch.group() == "years" or l_timeUnitMatch.group() == "year":
					l_TotalDays = float(l_numberMatch.group()) * 365
					print(l_numberMatch.group(), "Years in Days:", l_TotalDays)	

				if l_timeUnitMatch.group() == "months" or l_timeUnitMatch.group() == "month":
					l_TotalDays = float(l_numberMatch.group()) * 30.4167
					print(l_numberMatch.group(),"Months as Days:", l_TotalDays)	

			else:
				# # remove following single line to undo error report
				# print("\n")
				# print(a_TestString)
				print("ERROR: Found sentence: [", a_SentenceTypeMatch.group(), "], number: [", l_numberMatch.group(),"] but no time unit")
				print("ERROR: location ", l_numberMatch.group())
		
		else:
			# remove following single line to undo error report
			# print("\n")
			# print(a_TestString)
			print("ERROR: Found sentence: [", a_SentenceTypeMatch.group(), "] but no duration")
			print("ERROR: location: ", a_TestString[a_SentenceTypeMatch.start():len(a_TestString)])
	
	else:	
		# remove following single line to undo error report
		# print("\n")
		# print(a_TestString)
		print("ERROR: Found sentence: [", a_SentenceTypeMatch.group(), "] but no valid connectors")
		print("ERROR: location: ", a_TestString[a_SentenceTypeMatch.start():len(a_TestString)])


def searchForSetenceAndDuration(a_TestString):
	detentionMatch = re.search('detention', a_TestString)
	if detentionMatch:
		return searchDuration(a_TestString, detentionMatch)

	communityMatch = re.search('(communitycorrections?order|cco)', a_TestString)
	if communityMatch:
		searchDuration(a_TestString, communityMatch)

	nonparoleMatch = re.search('(non-? ?parole)', a_TestString)
	if nonparoleMatch:
		searchDuration(a_TestString, nonparoleMatch)

	mintermMatch = re.search('minimumtermtobeservedbeforebeingeligibleforparoleof|minimumtermof|minimumterm|minimum', a_TestString)
	if mintermMatch:
		searchDuration(a_TestString, mintermMatch)



def test(a_Request):
	
	# if the button is pressed and a form POST request is made
	if a_Request.method == 'POST':
	
		# save the request
		form = a_Request.POST

		# retriever the info
		raw_info = form.get('test1')

		# process the info
		processed_info = convertWordToNumber(" ".join(raw_info.splitlines()).lower())

		# conduct search
		result = searchForSetenceAndDuration(processed_info)

		# Print results of search to view for now
		messages.info( a_Request, {result} )

	return render(a_Request, 'sentenceRetiever/test.html')


