"""The functions required to classify galaxies as well as train on the previously
classified sample.

The order in which we do things
1. Load the cutouts.
2. Remove the cutouts that are already classified.
3. Loop over each cutout
    a. Display cutout
    b. Give morphology
    c. Give flags
    d. Save the morphology and flags
"""

import os


def run_train():
    """Run the training set of cutouts.

    This code loads the cutouts that were previously used as a training sample
    and tests the user. Will report back a score based on broad E/S0/Sp/Irr etc.
    """

    print "training"
    return


def run_classify(testing=''):
    """Runs the classification pipeline.

    This is the main body of code that will display the image cutouts and request
    classifications and flags.

    Parameters
    ----------
    testing : string
        When testing, the input/output files are read/saved from a different directory.
        This string is how we tell the function to look elsewhere for the files.
    """

    cutouts = load_cutout_list('{}cutoutlist.dat'.format(testing))
    # Check if user is mid-classification
    cutouts = gals_done(cutouts, testing)
    print "Beginning classification of {0} galaxies.".format(len(cutouts))

    # Loop over the cutout list
    for cutout in cutouts:
        display_gal(cutout)
        morph = classify_gal()
        if morph.lower() == 'q':
            break
        flags = set_flags()
        save_morph(cutout, morph, flags, testing)

    return


def load_cutout_list(cutoutlist):
    """Load the galaxy cutouts from a list of files.

    Parameters
    ----------
    cutoutlist : string
        The filename containing the list of paths to image cutouts.

    Returns
    -------
    fnames : list(string)
        List containing the path to a cutout as each element.
    """

    with open(cutoutlist) as fin:
        fnames = fin.readlines()
    fnames = [d_.strip('\n') for d_ in fnames]
    return fnames


def gals_done(fnames, testing=''):
    """Determine which cutouts have already been classified.

    Take the full list of cutout paths and subtract the list of classified cutout paths.

    Parameters
    ----------
    fnames : list(string)
        List containing the path to a cutout as each element.

    testing : string
        When testing, the input/output files are read/saved from a different directory.
        This string is how we tell the function to look elsewhere for the files.

    Returns
    -------
    todo_cutouts : list(string)
        List containing the paths to each cutout that is not yet classified.
    """

    inprog = os.path.exists('{}results.dat'.format(testing))

    if not inprog:
        return fnames

    with open('{}results.dat'.format(testing)) as done:
        done_fnames = done.readlines()
    done_fnames = [d_.split()[0].strip('\n') for d_ in done_fnames]
    todo_cutouts = list(set(fnames)-set(done_fnames))

    return todo_cutouts


def display_gal(fname):
    """Open a DS9 window for the cutout being classified.

    Parameters
    ----------
    fname : string
        Full path to the cutout being classified.
    """

    print "==========================================================="
    print "Displaying cutout {}".format(fname)
    print "DISPLAY NOT SET UP"
    return


def classify_gal():
    """Classify the cutout currently being displayed.

    This function first prints a list of options to the terminal and then asks
    the user to input a morphology.

    Returns
    -------
    morph : str
        The morphology of the currently displayed galaxy.
    """

    print_morph_options()
    morph = raw_input('Please enter a morphology.')
    return morph


def print_morph_options():
    """Print the options for the morphologies to the terminal.
    """

    print 'For spirals+, a slash is allowed if you are on the edge (1/3 for Sa/Sb)'
    print '-7 : Star'
    print '-6 : Non-stellar but compact'
    print '-5 : Elliptical'
    print '-2 : S0'
    print ' 1 : Sa'
    print ' 3 : Sb'
    print ' 5 : Sc'
    print ' 7 : Sd'
    print ' 9 : Sm'
    print '11 : Irr'
    print '66 : Unclassifiable'
    print ' q : Quit (progress is saved)\n\n'
    return


def set_flags():
    """Set flags for the currently displayed galaxy.

    This function first prints a list of options to the terminal and then asks
    the user to input flags.

    Returns
    -------
    flags : str
        The flags set for the current galaxy.
    """

    print_flag_options()
    flags = raw_input('Please enter flags (for both flag 2 and 3, enter \'23\' e.g.).')
    return flags


def print_flag_options():
    """Print the options for the flags to the terminal.
    """

    print '1. SODISK'
    print '2. BAR'
    print '3. EDGEON'
    print '4. SMALL'
    print '5. LSB'
    print '6. DEFECT'
    print '7. DUST'
    print '8. DISTURBED\n\n'
    return


def save_morph(fname, morph, flags, testing=''):
    """Save the morphology and flags to a results file.

    After the user has classified and set flags for a galaxy cutout, we then save
    on the fly to allow the user to quit at any time.

    Parameters
    ----------
    fname : str
        Full path to the cutout being classified.

    morph : str
        The morphology of the currently displayed galaxy.

    flags : str
        The flags set for the current galaxy.

    testing : str
        When testing, the input/output files are read/saved from a different directory.
        This string is how we tell the function to look elsewhere for the files.
    """

    with open('{}results.dat'.format(testing), 'a+') as fout:
        fout.write('{0} {1} {2}\n'.format(fname, morph, flags))
    return
