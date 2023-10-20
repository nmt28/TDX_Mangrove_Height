from rios import applier
from rios import cuiprogress
import argparse
import numpy as np

def MASKimage(info, inputs, outputs):

    # The interesting bit

    # Read in images as arrays
    TDX = inputs.image1.astype(np.float32)
    GLO = inputs.image2.astype(np.float32)
    DIFF = inputs.image3.astype(np.float32)

    tmp = np.where(DIFF>30, GLO, TDX).astype(np.float32)
    tmp_65 = np.where(tmp>60, 0, tmp)
    out = np.where(tmp_65>0.5, tmp_65, 0)

    outputs.outimage = out



def main():
    # Parse your arguments in
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--tdx", type=str, help="Specify the input WV")
    parser.add_argument("-g", "--glo", type=str, help="Specify the mask dataset")
    parser.add_argument("-d", "--diff", type=str, help="Specify the mask dataset")
    parser.add_argument("-o", "--output", type=str, help="Specify the output")
    args = parser.parse_args()
    # check file validity

    # Give the inputs names to associate them with in the function
    inputs = applier.FilenameAssociations()
    inputs.image1 = args.tdx
    inputs.image2 = args.glo
    inputs.image3 = args.diff

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
