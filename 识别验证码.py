#coding=utf-8
from PIL import Image
import math
import os
#import hashlib
#import time
image=Image.open("4wc2fa.gif")
#将图片转化为8位像素格式
image.convert("P")
#打印颜色直方图
#print image.getcolors()
#print image.histogram()
his=image.histogram()
values={}
for i in xrange(256):
	values[i]=his[i]
#print values
#进行排序
for j,k in sorted(values.items(),key=lambda x:x[1],reverse=True)[:10]:
	#降序排列,取颜色像素点排在前十的颜色序列
	print j,k
#然后构造二值图
image2=Image.new("P",image.size,255)
for x in range(image.size[0]):
	for y in range(image.size[1]):
		pixel=image.getpixel((x,y))
		# if pixel<=226 and pixel>=220:
		if pixel==227 or pixel==220:#更改此处会造成二值图线条发生变化，影响向量识别
			image2.putpixel((x,y),0)
image2.show()
#提取单个图片
inletter=False
foundletter=False
start=0
end=0
letters=[]
for x in xrange(image2.size[0]):
	pixcount=0
	for y in xrange(image2.size[1]):
		pixel=image2.getpixel((x,y))
		if pixel!=255:
			pixcount+=1
			inletter=True
	# if pixcount<=3:
		# inletter=True
	if inletter==True and foundletter==False:
		foundletter=True
		start=x
	# if inletter==False and foundletter==True:
	if pixcount<=1 and foundletter==True:
		foundletter=False
		end=x
		letters.append((start,end))
	inletter=False
print letters
# #对图片进行切割，得到字符所在位置的图片
# count=['1','2','3','4','5','6']
# key=0
# for letter in letters:
# 	image3=image2.crop((letter[0],0,letter[1],image2.size[1]))
# 	image3.save("%s.gif"%count[key])
# 	key+=1
#用python类写向量空间
class VectorCompare:
	#计算适矢量大小
	def magnitude(self,concordance):
		total=0
		for word,count in concordance.iteritems():
			total+=count**2
		return math.sqrt(total)
	#计算矢量间cos值
	def relation(self,concordance1,concordance2):
		relevance=0
		topvalue=0
		for word,count in concordance1.iteritems():
			if concordance2.has_key(word):
				topvalue+=count*concordance2[word]
		return topvalue/(self.magnitude(concordance1)*self.magnitude(concordance2))
#将图片转化为矢量
def buildvector(im):
	d1={}
	count=0
	for i in im.getdata():#返回一个图像的像素值序列
		d1[count]=i
		count+=1
	return d1
v=VectorCompare()
iconset=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
#加载训练集
imageset=[]
for letter in iconset:
	for img in os.listdir("./iconset/%s/"%letter):
		temp=[]
		if img!='Thumbs.db' and img !=".DS_Store":
			temp.append(buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
		imageset.append({letter:temp})
#对图片进行切割，得到字符所在位置的图片
count=['1','2','3','4','5','6']
key=0
for letter in letters:
	image3=image2.crop((letter[0],0,letter[1],image2.size[1]))
	image3.save("%s.gif"%count[key])
	guess=[]
	#将分割的验证码的每一片段和每个训练片段比较
	for image in imageset:
		for x,y in image.iteritems():
			if len(y)!=0:
				guess.append((v.relation(y[0],buildvector(image3)),x))
	guess.sort(reverse=True)
	print "",guess[0]
	key+=1