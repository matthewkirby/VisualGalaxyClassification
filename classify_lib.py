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
import easygui as eg
import pyds9 as ds9
from random import shuffle


def run_train():
    """Run the training set of cutouts.

    This code loads the cutouts that were previously used as a training sample
    and tests the user. Will report back a score based on broad E/S0/Sp/Irr etc.
    """

    cutouts = load_cutout_list('training/traininglist.dat')
    print "Beginning training on {0} galaxies.".format(len(cutouts))
    print "All training objects have a single classification and no flags."

    morph_choices = fetch_morph_options()
    classifications = []

    # Loop over the cutout list
    for cutout in cutouts:
        display_gal('training/training_cutouts/'+cutout)
        morph = classify_gal(morph_choices)
        if morph == 'Quit':
            break
        classifications.append([cutout, morph])

    calc_training_score(classifications)
    return


def fetch_training_truth():
    """Load the truth for the training set.

    Returns
    -------
    truths : list(str,str)
        Each element in the list is a tuple. The first element is the cutout name,
        the second element is the classification.
    """
    with open('training/training_truth.dat', 'r') as fin:
        truths = fin.readlines()
    truths = [t_.split() for t_ in truths]
    return truths


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
    cutouts = gals_done(cutouts, testing)
    print cutouts[0]
    shuffle(cutouts)
    print cutouts[0]
    print "Beginning classification of {0} galaxies.".format(len(cutouts))

    morph_choices = fetch_morph_options()
    flag_choices = fetch_flag_options()

    # Loop over the cutout list
    for cutout in cutouts:
        display_gal('cutouts/'+cutout)
        morph = classify_gal(morph_choices)
        if morph == 'Quit':
            break
        flags = set_flags(flag_choices)
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


def fetch_morph_options():
    """Load the morphology options.

    Morphology options are read in from a file in the tables subdir

    Returns
    -------
    opts : list(str)
        The list of classification options
    """

    with open('tables/classification_options.dat', 'r') as fin:
        opts = fin.readlines()
    opts = [opt.strip('\n') for opt in opts]

    return opts


def fetch_flag_options():
    """Load the flag options.

    Flag options are read in from a file in the tables subdir

    Returns
    -------
    opts : list(str)
        The list of flag options
    """

    with open('tables/flag_options.dat', 'r') as fin:
        opts = fin.readlines()
    opts = [opt.strip('\n') for opt in opts]

    return opts


def display_gal(fname):
    """Open a DS9 window for the cutout being classified.

    Parameters
    ----------
    fname : string
        Full path to the cutout being classified.
    """

    print "==========================================================="
    print "Displaying cutout {}".format(fname)

    ds9window = ds9.DS9()
    ds9window.set("tile yes")
    ds9window.set("tile mode column")

    ds9window.set("frame 1")
    ds9window.set("file " + fname)
    ds9window.set("zoom to fit")
    ds9window.set("scale log")
    #ds9window.set("scale limits -0.1 2")

    ds9window.set("frame 2")
    ds9window.set("file " + fname)
    ds9window.set("zoom to fit")
    ds9window.set("scale log")
    ds9window.set("scale limits -0.1 25")

    return


def classify_gal(choices):
    """Classify the cutout currently being displayed.

    This function first prints a list of options to the terminal and then asks
    the user to input a morphology.

    Parameters
    ----------
    choices : list(str)
        The list of classification options

    Returns
    -------
    morph : str
        The morphology of the currently displayed galaxy.
    """

    morph = ''
    while True:
        newmorph = eg.buttonbox("Please enter galaxy classification.\n"
                                "Current class: {}".format(morph), choices=choices,
                                default_choice='Next', cancel_choice='Quit')
        if newmorph == 'Reset':
            morph = ''
            continue
        elif newmorph == 'Next':
            if morph == '':
                continue
            break
        elif newmorph == 'Quit':
            return 'Quit'
        morph += '{}|'.format(newmorph)

    return morph[:-1]


def set_flags(choices):
    """Set flags for the currently displayed galaxy.

    This function first prints a list of options to the terminal and then asks
    the user to input flags.

    Returns
    -------
    flags : str
        The flags set for the current galaxy.
    """

    flags = ''
    while True:
        newflag = eg.buttonbox("Please select all applicable flags. Press done when you are "
                               "finished.\nCurrenltly selected: {}".format(flags), choices=choices,
                               default_choice='Done', cancel_choice='Done')
        if newflag == 'Reset':
            flags = ''
            continue
        if newflag == 'Done':
            break
        flags += '{}|'.format(newflag)

    return flags[:-1]


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


def calc_training_score(classifications):
    """Take the classifications and compare to the truth for the training sample.

    Parameters
    ----------
    classifications : list(str, str)
        Each element in the list is a tuple. The first element is the cutout name,
        the second element is the classification.
    """

    trueclassifications = fetch_training_truth()
    full, rough = [], []

    for usermorph in classifications:
        trueclass = ''

        for truth in trueclassifications:
            if usermorph[0] == truth[0]:
                trueclass = truth[1]
                break

        if trueclass == usermorph[1]:
            full.append(1.)
            rough.append(1.)
        elif check_broad_training_categories(trueclass, usermorph[1]):
            full.append(0.)
            rough.append(1.)
        else:
            full.append(0.)
            rough.append(0.)

    print "=========================================="
    print "================ Summary ================="
    print "Classified {} galaxies out of the training set of {}".format(
        len(classifications), len(trueclassifications))
    print "Score (Bad/E/S0/Sp/Irr bins): {:.1f}".format(100.*sum(rough)/len(rough))
    print "Score (Full bin resolution): {:.1f}".format(100.*sum(full)/len(full))


def check_broad_training_categories(truth, clmorph):
    """Check the broad categories for spirals/irregulars/bad cutouts

    Parameters
    ----------
    truth : str
        The true classification of the object

    clmorph : str
        The user classification of the object
    """
    spirals = ['Sa', 'Sb', 'Sc', 'Sd']
    irregulars = ['Sm', 'Irr']
    bads = ['Star', 'Compact,-not-star', 'Unclassifiable']

    if truth in spirals and clmorph in spirals:
        return True
    elif truth in irregulars and clmorph in irregulars:
        return True
    elif truth in bads and clmorph in bads:
        return True
    return False
