import os
from pathlib import Path
import tifffile as tiff
from PIL import Image
from scipy import ndimage


def int16_to_int8(img16):
    image8 = (img16/256).astype('uint8')
    return image8


init = 'D:/Image Processing Project/datasets/'
final13 = 'D:\Image Processing Project\mrg\k_3//'
final15 = 'D:\Image Processing Project\mrg\k_5//'
final2 = 'D:\Image Processing Project\gr\\'
imageLoc = [['giantin', 'hoechst', 'lamp2', 'nop4', 'tubulin'],
            ['pictures'],
            ['CG10873', 'CG12284', 'CG1258', 'CG17161', 'CG3733', 'CG3938', 'CG7922', 'CG8114', 'CG8222', 'CG9484'],
            ['resampled-to-8bit']]
imageSets = ['CH//cho//',
             'PI//bible_dataset\\',
             'RN//rn//',
             'VI//']

c = 0
for i in range(len(imageLoc)):
    for j in range(len(imageLoc[i])):
        # Forming file Paths
        filePath = init + imageSets[i] + imageLoc[i][j]
        p = Path(filePath)

        for x in p.iterdir():
            if x.suffix == '.tiff' or x.suffix == '.tif':
                image16 = tiff.imread(str(x))
            elif x.suffix == '.png' or x.suffix == '.jpg':
                image16 = ndimage.imread(str(x))
            else:
                continue

            if image16.dtype == 'uint16':
                img8 = int16_to_int8(image16)
            else:
                img8 = image16

            # Applying the Gaussian Mask k=3,5 and SD=1.0
            gauss3 = ndimage.gaussian_filter(img8, 1, mode='wrap')
            gauss5 = ndimage.gaussian_filter(img8, 1, mode='wrap')

            # Finding the Gradient Image
            gi = ndimage.sobel(img8, 1, mode='wrap')

            # Forming Images from Array
            Gauss3 = Image.fromarray(gauss3)
            Gauss5 = Image.fromarray(gauss5)
            GI = Image.fromarray(gi)

            # Forming Save file Paths
            w = str(x)
            y3 = os.path.normpath(final13 + imageSets[i] + imageLoc[i][j] + '//' + w[w.rfind('\\')+1: w.rfind('.')]) + x.suffix
            y5 = os.path.normpath(final15 + imageSets[i] + imageLoc[i][j] + '//' + w[w.rfind('\\')+1: w.rfind('.')]) + x.suffix
            gr = os.path.normpath(final2 + imageSets[i] + imageLoc[i][j] + '//' + w[w.rfind('\\')+1: w.rfind('.')]) + x.suffix
            # print(gr) - Checks if the program is running or not

            # Saving Images
            Gauss3.save(str(y3))
            Gauss5.save(str(y5))
            GI.save(str(gr))

            c = c+1

print('Total FILES Processed : ', c, end=' ')
print()
