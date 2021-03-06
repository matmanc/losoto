LoSoTo: LOFAR solutions tool
============================

Main developer:
* Francesco de Gasperin

Contributed code:
* David Rafferty
* Maaijke Mevius
* Jose Sabater Montes
* Martin Hardcastle
* Andreas Horneffer
* and the LOFAR Survey Key Science Project

Cite:
* If you use LoSoTo for your data reduction, please cite: de Gasperin et al. 2019, Astronomy & Astrophysics, Volume 622, id.A5
(https://ui.adsabs.harvard.edu/abs/2019A&A...622A...5D/abstract)


Install:
* Get LoSoTo from https://github.com/revoltek/losoto 
* Install losoto by simply: python setup.py install --prefix=~/mydir/
* Alternatively: pip install --upgrade --user https://github.com/revoltek/losoto/archive/master.zip 
* In cep3 use the copy of the code in ~fdg/scripts/losoto/ (source the tool/lofarinit.[c]sh file which is shipped with the code)
* Prepare a parset starting from the parset/losoto2.parset
* in case of problems write to Francesco de Gasperin: astro@voo.it

Documentation:
* Documentation of LoSoTo API is at: __http://revoltek.github.io/losoto/losoto.html__
* A detailed explanation of all the parameters is at: __http://revoltek.github.io/losoto/losoto.operations.html__
* A few important articles/how-to are on the github wiki: __https://github.com/revoltek/losoto/wiki__

Contents:
* __bin/__: the losoto executable and some manipulators for H5parms
* __docs/__: documentation
* __examples/__: some examples h5parm to use with validation/test parsets
* __losoto/operations/__: containts all the modules for operations
* __parsets/__: some examples parsets
* __tools/__: contains some external tools

Required packages:
* Python 3
* PyTables version:  >3.4.0
* HDF5 version:      >1.8.4
* NumPy version:     >1.9.0
