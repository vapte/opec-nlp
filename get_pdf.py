import requests


def get_pdf(month, year):   #both inputs are strs
    
    r = get_response(month, year)

    local_file = open('output/'+'_'.join(['OPEC',month,year])+'.pdf', 'wb')
    local_file.write(r.content)
    local_file.close()
    if (len(r.content)<20000):
        print('url error', month, year)
        assert(0==1)    #this is a really ratchet error message
    else:
        print("good", month, year)
    return r.content

def get_response(month, year):
    url_mr= 'http://www.opec.org/opec_web/static_files_project/media/downloads/publications/MR'
    url_momr = 'http://www.opec.org/opec_web/static_files_project/media/downloads/publications/MOMR'

    delimiters = ['','_','%20']
    url_attempts = list()
    for delimiter in delimiters:    #OPEC has inconsistent URL formatting
        url_attempts.append(form_URL(month,year, delimiter))
    
    #MOMR_Month_Year_.pdf'
    url_attempts.append(url_attempts[1][:-4]+'_'+url_attempts[1][-4:]) 
    #MRmmyyyy
    url_attempts.append(url_mr+month2digit(month)+year+'.pdf')
    #MOMR_mmyyyy
    url_attempts.append(url_momr+'_'+month2digit(month)+year+'.pdf')

    r = None
    for url in url_attempts:
        r = requests.get(url)
        if (len(r.content)>20000):
            break
    return r

def month2digit(month):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November',
                'December']

    idx = months.index(month)+1

    if (idx<10):
        return '0'+str(idx)
    else:
        return str(idx)


def form_URL(month,year,delimiter):
    url= 'http://www.opec.org/opec_web/static_files_project/media/downloads/publications/MOMR'
    return url+delimiter+month+delimiter+year+'.pdf'


#.if __name__ == '__main__':
    months = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November',
                'December']

    years = [str(y) for y in range(2001,2017)]

    for year in years:
        for month in months:
            get_pdf(month, year)

