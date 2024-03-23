from inc_noesis import *


def registerNoesisTypes():
    handle = noesis.register("American Chopper (2004) images", ".csi")
    noesis.setHandlerTypeCheck(handle, amchrCheckType)
    noesis.setHandlerLoadRGBA(handle, amchrLoadRGBA)

    return 1
         
  
class AmchrTexture:
    def __init__(self, reader):
        self.filereader = reader
        self.width = 0
        self.height = 0
        self.format = 0
        self.bytesPerPixel = 0
 
    def parseHeader(self): 
        self.filereader.seek(16, NOESEEK_ABS) 
        self.width = self.filereader.readUInt()
        self.height = self.filereader.readUInt()
        self.bytesPerPixel = self.filereader.readUInt()
        self.filereader.seek(36, NOESEEK_ABS) 
        self.format = self.filereader.readUInt()
        self.filereader.seek(160, NOESEEK_ABS) 
        
        return 0

    def readImage(self):
        data = self.filereader.readBytes(self.width * self.height * self.bytesPerPixel) 

        format = {5392194: "b8g8r8", 
            4343634: "r8g8b8",
            1111970369: "b8g8r8p8"}
        self.data = rapi.imageDecodeRaw(data, self.width, self.height, format[self.format])       
         
    def read(self):
        self.parseHeader()
        self.readImage()
    
    
def amchrCheckType(data):
    img = AmchrTexture(NoeBitStream(data))
    if img.parseHeader() != 0:
        return 0
        
    return 1  


def amchrLoadRGBA(data, texList):
    #noesis.logPopup() 
    tex = AmchrTexture(NoeBitStream(data))       
    tex.read() 
     
    texList.append(NoeTexture("amchrtex", tex.width, tex.height, tex.data, noesis.NOESISTEX_RGBA32))
            
    return 1
