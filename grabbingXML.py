#thanks to https://github.com/stchris/untangle
import untangle
xmlObj = untangle.parse('https://api.bmreports.com/BMRS/FUELINSTHHCUR/v1?APIKey=po7f83ilmq2p223&ServiceType=XML')

# for item in xmlObj.response.responseBody.responseList.item:
#     fuelType = item.fuelType.cdata
#     currentMW = item.currentMW.cdata
#     if currentMW:
#         print(fuelType)
#         print(currentMW)
#         
gasMW = xmlObj.response.responseBody.responseList.item[0].currentMW.cdata
gasDescriptor = xmlObj.response.responseBody.responseList.item[0].fuelType.cdata

print(gasDescriptor)
print(gasMW)

# using https://www.foxinfotech.in/2019/04/python-how-to-read-xml-from-url.html

# from urllib.request import urlopen
# from xml.etree.ElementTree import parse
# 
# var_url = urlopen('https://api.bmreports.com/BMRS/FUELINSTHHCUR/v1?APIKey=po7f83ilmq2p223&ServiceType=XML')
# xmldoc = parse(var_url)
# 
# root = xmldoc.getroot()
# 
# # for child in root:
# #     print(child.tag, child.attrib)
# # Lists:
# # responseMetadata {}
# # responseHeader {}
# # responseBody {}
#     
# #this seems to not work, but not sure if because of rate limits
# # for x in root.findall('item'):
# #     fuelType = x.find('fuelType').text
# #     currentMW = x.find('currentMW').text
# #     print(fuelType, currentMW)
# 
# for elem in root.iterfind('response/responseBody/responseList/item'):
#     print(elem.tag)
#     print(elem.attrib)