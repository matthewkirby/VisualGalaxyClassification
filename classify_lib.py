import os
# When classifying, I want to append after each step
# Should be able to be reran and only need to look at unclassified things.
# Ask if it is first time or resuming, if resuming, open up the output file and drop things from the lsit of cutouts


##############################################
# Runs the training script
def run_train():
    print "training"
    pass


##############################################
# Runs the classification script
def run_classify(testing=''):
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


##############################################
# Load the cutouts from the file
def load_cutout_list(cutoutlist):
    with open(cutoutlist) as fin:
        fnames = fin.readlines()
    fnames = [d_.strip('\n') for d_ in fnames]
    return fnames


##############################################
# Check to see if user is mid classification
# If so, remove completed cutouts from the list
def gals_done(fnames, testing=''):
    if os.path.exists('{}results.dat'.format(testing)):
        inprog = True
    else:
        inprog = False

    if not inprog:
        return fnames

    with open('{}results.dat'.format(testing)) as done:
        done_fnames = done.readlines()
    done_fnames = [d_.split()[0].strip('\n') for d_ in done_fnames]
    fnames = list(set(fnames)-set(done_fnames))

    return fnames


##############################################
# Display the cutout being classified
def display_gal(fname):
    print "==========================================================="
    print "Displaying cutout {}".format(fname)
    print "DISPLAY NOT SET UP"
    return


##############################################
# Classify the currently displayed cutout
def classify_gal(testtext=''):
    print_morph_options()
    morph = raw_input('Please enter a morphology. {}'.format(testtext))
    return morph


##############################################
# Print the options for morphology
def print_morph_options():
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


##############################################
# Set an flags for the galaxy
# Flags are numbers from 0-7 and we just make a string of them
def set_flags():
    print_flag_options()
    flags = raw_input('Please enter flags (for both flag 2 and 3, enter \'23\' e.g.).')
    return flags


##############################################
# Print the options for flags
def print_flag_options():
    print '1. SODISK'
    print '2. BAR'
    print '3. EDGEON'
    print '4. SMALL'
    print '5. LSB'
    print '6. DEFECT'
    print '7. DUST'
    print '8. DISTURBED\n\n'
    return


##############################################
# Save the morphology to an outputfile
def save_morph(fname, morph, flags, testing=''):
    with open('{}results.dat'.format(testing), 'a+') as fout:
        fout.write('{0} {1} {2}\n'.format(fname, morph, flags))
    return


##############################################
# Required for testing purposes
# __builtins__ is instanciated differently when in __main__ module and in other module
# This function lets you overload the attributes regardless of which type it is
def set_builtin(name, value):
    if isinstance(__builtins__, dict):
        __builtins__[name] = value
    else:
        setattr(__builtins__, name, value)