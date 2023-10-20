from rios import applier
from rios import cuiprogress
import argparse
import numpy as np

def MASKimage(info, inputs, outputs):
    
    # The interesting bit
    
    # Read in images as arrays
    TDX = inputs.image1.astype(np.float32)
    GMW = inputs.image2.astype(np.float32)
    EGM = inputs.image3.astype(np.float32)
    WATER = inputs.image4.astype(np.float32)
    
    
    tmp = np.where((GMW==1) & (WATER==0), (TDX-EGM), 0).astype(np.float32)
    out = np.where((GMW==1) & (WATER==0) & (tmp<-500), 500, tmp).astype(np.float32)
    
    #out = np.where(tmp > 70, 70, tmp)
    
    outputs.outimage = out



def main():
    # Parse your arguments in
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--tdx", type=str, help="Specify the input WV")
    parser.add_argument("-g", "--gmw", type=str, help="Specify the mask dataset")
    parser.add_argument("-e", "--egm08", type=str, help="Specify the mask dataset")
    parser.add_argument("-w", "--watermask", type=str, help="Specify the mask dataset")
    parser.add_argument("-o", "--output", type=str, help="Specify the output")
    args = parser.parse_args()
    # check file validity
    
    # Give the inputs names to associate them with in the function
    inputs = applier.FilenameAssociations()
    inputs.image1 = args.tdx
    inputs.image2 = args.gmw
    inputs.image3 = args.egm08
    inputs.image4 = args.watermask
    
    outfiles = applier.FilenameAssociations()
    outfiles.outimage = args.output
    
    # Set up some of the environment controls - a progress bar, filetype...
    # setReferenceImage is the file to use as the master if your inputs are not in the same projection etc
    aControls = applier.ApplierControls()
    aControls.progress = cuiprogress.CUIProgressBar()
    aControls.drivername = 'GTiff'
    aControls.setReferenceImage(inputs.image1)
    aControls.setCreationOptions("COMPRESS=LZW", "BIGTIFF=IF_SAFER")
    aControls.setCalcStats(False)
    #aControls.setApproxStats(True)
    
    # Run function
    applier.apply(MASKimage, inputs, outfiles, controls=aControls)


if __name__ == "__main__":
    main()

