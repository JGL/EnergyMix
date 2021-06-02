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
gasMW = float(xmlObj.response.responseBody.responseList.item[0].currentMW.cdata)
gasDescriptor = xmlObj.response.responseBody.responseList.item[0].fuelType.cdata

coalMW = float(xmlObj.response.responseBody.responseList.item[3].currentMW.cdata)
coalDescriptor = xmlObj.response.responseBody.responseList.item[3].fuelType.cdata

nuclearMW = float(xmlObj.response.responseBody.responseList.item[4].currentMW.cdata)
nuclearDescriptor = xmlObj.response.responseBody.responseList.item[4].fuelType.cdata

windMW = float(xmlObj.response.responseBody.responseList.item[5].currentMW.cdata)
windDescriptor = xmlObj.response.responseBody.responseList.item[5].fuelType.cdata

pumpedStorageHydroMW = float(xmlObj.response.responseBody.responseList.item[6].currentMW.cdata)
pumpedStorageHydroDescriptor = xmlObj.response.responseBody.responseList.item[6].fuelType.cdata

nonPumpedHydroMW = float(xmlObj.response.responseBody.responseList.item[7].currentMW.cdata)
nonPumpedHydroDescriptor = xmlObj.response.responseBody.responseList.item[7].fuelType.cdata

totalHydro = pumpedStorageHydroMW + nonPumpedHydroMW

biomassMW = float(xmlObj.response.responseBody.responseList.item[13].currentMW.cdata)
biomassDescriptor = xmlObj.response.responseBody.responseList.item[13].fuelType.cdata

timeLastUpdated = xmlObj.response.responseBody.dataLastUpdated.cdata

print(gasDescriptor)
print(gasMW)
print(coalDescriptor)
print(coalMW)
print(nuclearDescriptor)
print(nuclearMW)
print(windDescriptor)
print(windMW)
print(pumpedStorageHydroDescriptor)
print(pumpedStorageHydroMW)
print(nonPumpedHydroDescriptor)
print(nonPumpedHydroMW)
print("Total hydro:")
print(totalHydro)
print(biomassDescriptor)
print(biomassMW)
print("Time last updated:")
print(timeLastUpdated)