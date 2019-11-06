from django.shortcuts import render

def home(a_Request):
	return render(a_Request, 'LandingPage/home.html', {'title':'Home'})

def about(a_Request):
	return render(a_Request, 'LandingPage/about.html', {'title':'About'})

def documentation(a_Request):
	return render(a_Request, 'LandingPage/documentation.html', {'title':'Documentation'})

def orange(a_Request):
	return render(a_Request, 'LandingPage/orange.html', {'title':'Orange'})

def stats(a_Request):
	return render(a_Request, 'LandingPage/stats.html', {'title':'Statistics'})

def tools(a_Request):
	return render(a_Request, 'LandingPage/tools.html', {'title':'Tools'})

def docs(a_Request):
	return render(a_Request, 'LandingPage/docs.html', {'title':'Documentation'})

def StatsDocumentation(a_Request):
	return render(a_Request, 'LandingPage/StatsDocumentation.html', {'title':'Stats Documentation'})

def OrangeDocumentation(a_Request):
	return render(a_Request, 'LandingPage/OrangeDocumentation.html', {'title':'Orange Documentation'})

def WebsiteDocumentation(a_Request):
	return render(a_Request, 'LandingPage/WebsiteDocumentation.html', {'title':'Website Documentation'})

def ProcessDocumentation(a_Request):
	return render(a_Request, 'LandingPage/ProcessDocumentation.html', {'title':'Process Documentation'})

def results(a_Request):
	return render(a_Request, 'LandingPage/results.html', {'title':'Results'})

def gui(a_Request):
	l_Context = {
		# 'info':testData,
		'title': 'GUI',
	}
	return render(a_Request, 'LandingPage/gui.html', l_Context)


def testPage(a_Request):
	l_Context = {
		'info':testData,
		'title': 'testPage',
	}

	return render(a_Request, 'LandingPage/testPage.html', l_Context)
