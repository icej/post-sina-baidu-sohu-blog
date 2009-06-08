#!/usr/bin/env python
# encoding: utf-8
import urllib,urllib2,httplib,cookielib,os,re,sys,time,md5,copy
def getData ():
	data=[]
	content = '''内容'''
	data.append({"content":content,"title":"标题","tag":"tag"})
	return data

def login(userdata,posturl):
	print userdata
	cookie=cookielib.CookieJar()
	cj=urllib2.HTTPCookieProcessor(cookie)
	request=urllib2.Request(posturl)
	opener=urllib2.build_opener(cj)
	c = opener.open(request,urllib.urlencode(userdata))
	bincontent= c.read()
	return opener

#baidu用
def connection (data,method,host,url,headers):
	print "---request---"
	print data,method,host,url,headers
	conn=httplib.HTTPConnection(host)
	data = urllib.urlencode(data)
	conn.request(method,url,data,headers)
	res=conn.getresponse()
	cookie=re.split(r',',res.getheader('set-cookie'))
	print "---get cookie---"
	print cookie
	if not headers.has_key("cookie"):
		headers['cookie']=""
	for c in cookie:
		b=re.split(r';',c)
		b=b[0].strip()
		if b[0]=="B":
			if headers['cookie']=="":
				headers['cookie']=b
			else:
				headers['cookie']=headers['cookie']+';'+b
	res.close()
	return headers

def postdata (opener,data,posturl):
	loginrequest=urllib2.Request(posturl)
	c = opener.open(loginrequest,urllib.urlencode(data))
	bincontent = c.read()
	return bincontent

def postsohu (username,passwd):
	m = md5.md5(passwd)
	userdata = {'appid':'1019','b':'1','password':m.hexdigest(),
	'persistentcookie':0,'pwdtype':'1','s':'1213527861109','userid':username+'@sohu.com','w':'1280'}
	data = getData()
	opener = login(userdata,'http://passport.sohu.com/sso/login.jsp?userid='+username+'%40sohu.com&password='+userdata['password']+'&appid=1019&persistentcookie=0&s=1213527861109&b=1&w=1280&pwdtype=1')
	while len(data)>0:
		d = data.pop()
		postpage=urllib2.Request('http://blog.sohu.com/manage/entry.do?m=add&t=shortcut')
		c = opener.open(postpage)
		bincontent= c.read()
		p=re.compile(r'''\s+<input type="hidden" name="aid" value="(.*)">\s+''',re.M)
		c = p.findall(bincontent)
		print c
		if len(c)>0:
			sohudata = {'aid':c[0],'allowComment':2,'categoryId':0,'contrCataId':'','contrChId':''
			,'entrycontent':unicode(d['content'],"utf-8").encode("gbk"),'entrytitle':unicode(d['title'],"utf-8").encode("gbk"),'excerpt':'',
			'keywords':unicode(d['tag'],"utf-8").encode("gbk"),'m':'save','newGategory':'','oper':'art_ok','perm':'0','save':'-','shortcutFlag':'true'}
			#print sohudata
			postdata(opener,sohudata,'http://blog.sohu.com/manage/entry.do')


def postsina (username,passwd):
	userdata = {'loginname':username,'passwd':passwd}
	opener = login(userdata,'http://my.blog.sina.com.cn/login.php?index=index&type=new')
	data = getData()
	while len(data)>0:
		d = data.pop()
		postpage=urllib2.Request('http://control.blog.sina.com.cn/admin/article/article_add.php')
		c = opener.open(postpage)
		bincontent= c.read()
		p=re.compile(r'''\s+<input type="hidden" name="vtoken" value="(.*)"/>\s+''',re.M)
		c = p.findall(bincontent)
		print c
		if len(c)>0:
			sinadata = {'album':'','blog_body':d['content'],'blog_class':0,
			'blog_id':'','blog_title':d['title'],'is2bbs':1,'is_album':0,'is_media':'0',
			'join_circle':1,'sina_sort_id':'105','newsid':'','sno':'','stag':'','tag':d['tag'],'time':'','x_cms_flag':1,'url':'','vtoken':c[0]}
			postdata(opener,sinadata,'http://control.blog.sina.com.cn/admin/article/article_post.php')
			time.sleep(70)

def postbaidu (username,passwd):
	headers={'Connection':'Keep-Alive',
	'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 2.0.50727; .NET CLR 1.1.4322)',
	'domain':'baidu.com'
	}
	hihost='hi.baidu.com'
	#获得cookie
	headers = connection('','GET',hihost,'/',headers)
	#登录
	passhost='passport.baidu.com'
	userdata={'username':username,'password':passwd,'mem_pass':'on'}
	headers = connection(userdata,'POST',passhost,'/?login',headers)
	#发日志
	data = getData()
	while len(data)>0:
		d = data.pop()
		try:
			baidudata = {'cm':1,'ct':1,'spBlogCatName':unicode('默认分类',"utf-8").encode("gb2312"),'spBlogPower':0,'spBlogText':unicode(d['content'],"utf-8").encode("gb2312")
			,'spBlogTitle':unicode(d['title'],"utf-8").encode("gb2312"),'spIsCmtAllow':1,'spRefURL':'http://hi.baidu.com/icejtest22/creat/blog/',
			'spVcode':'','spVerifyKey':'','tj':''}
			headers = connection(baidudata,'POST',hihost,'/%s/commit' %(username),headers)
		except Exception:
			print "data error\r\n"
def main ():
	sohupassport =[{'user':'user','passwd':'123456'}]
	sinapassport =[{'user':'user','passwd':'123456'}]
	baidupassport =[{'user':'user','passwd':'123456a'}]
	print "SOHU USER %s\r\n" %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	for users in sohupassport:
		print "user:%s\r\n" % (users["user"])
		#postsohu(users["user"],users["passwd"])
	print "SINA USER %s\r\n" %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	for users in sinapassport :
		print "user:%s\r\n" % (users["user"])
		#postsina (users["user"],users["passwd"])
	for users in baidupassport :
		print "user:%s\r\n" % (users["user"])
		postbaidu (users["user"],users["passwd"])
if __name__ == '__main__':
    main()
