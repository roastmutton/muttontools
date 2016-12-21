
"""
Nose tests for file reader and writer.

Use:

    >>> nosetests

Test directory includes the test files:

    *
    *
"""

import os

from muttontools.col_readwrite import readcol, writecol
from nose.tools import *
from IPython.utils.capture import capture_output


# Tests for readcol

def test_reads_nominal_file():
    assert readcol(filename='nominal.txt') == (['x', 'y'], [['1', '2', '3', '4'], ['.1', '.2', '.3', '.4']])

def test_skips_custom_comment_lines():
    assert readcol(filename='comments_custom.txt', comment='%') == ([], []) 
    assert readcol(filename='comments_custom2.txt', comment='%') == (['x', 'y'], [['1', '2', '3'], ['.1', '.2', '.3']])

def test_exits_gracefully_if_no_file():
    assert readcol(filename='noexistence.txt') == ([], [])

def test_finds_header_and_data_if_not_default():
    assert readcol(filename='nondefault_start.txt', headerstart=4, datastart=6) == (['x', 'y'], [['1', '2', '3', '4'], ['.1', '.2', '.3', '.4']])

def test_reads_empty_file_gracefully():
    assert readcol(filename='empty.txt') == ([], [])

def test_can_mix_space_and_tab():
    assert readcol(filename='mixed_space_tab.txt') == (['x', 'y'], [['1', '2', '3', '4'], ['.1', '.2', '.3', '.4']])

def test_can_read_custom_deliminator():
   assert readcol(filename='custom_deliminator.txt', deliminator="|") == (['x', 'y'], [['1', '2', '3', '4'], ['.1', '.2', '.3', '.4']])

def test_can_read_single_column_file():
    assert readcol(filename='single_col.txt') == (['x'], [['1', '2', '3', '4']])    

def test_can_read_no_header():
    assert readcol(filename='noheader.txt', headerstart=0, datastart=0) == (['0', '1'], [['1', '2', '3', '4'], ['.1', '.2', '.3', '.4']])


# Tests for writecol

def test_writes_nominal_file():
    """ If this test does not work, all remaining tests will fail 
    because rely on generation of a nominal file. 
    """
    filename='nominal_write.txt'
    writecol(filename=filename, data=[['1', '2', '3', '4'], ['.1', '.2', '.3', '.4']], header=['x', 'y'])
    assert readcol(filename=filename) == (['x', 'y'], [['1', '2', '3', '4'], ['.1', '.2', '.3', '.4']])
    os.remove(filename)

def test_doesnt_modify_file_if_overwrite_False():
    filename='test_overwrite_false.txt'
    writecol(filename=filename, data=[['1', '2', '3', '4'], ['.1', '.2', '.3', '.4']], header=['x', 'y'])
    with capture_output() as c:
        writecol(filename=filename, data=[['1', '2', '3', '4'], ['.1', '.2', '.3', '.4']], header=['x', 'y'], overwrite=False)
    c()
    out = c.stdout
    assert out.split('\n')[0] == "File '{}' already exists and overwrite is set to False. Halting...".format(filename)
    os.remove(filename)

def test_does_append_file_if_overwrite_True():
    """ writer = 'a+'
    """
    filename='test_append_overwrite_true.txt'
    writecol(filename=filename, data=[['1', '2', '3', '4'], ['.1', '.2', '.3', '.4']], header=['x', 'y']) 
    with capture_output() as c:
        writecol(filename=filename, data=[['5', '6'], ['.5', '.6']], writer='a+', overwrite=True)
    c()
    out = c.stdout
    assert out.split('\n')[0] == "File '{}' already exists but overwriting/appending with '{}'..."\
        .format(filename, 'a+')
    assert readcol(filename=filename) == (['x', 'y'], [['1', '2', '3', '4', '5', '6'], ['.1', '.2', '.3', '.4', '.5', '.6']])
    os.remove(filename)

def test_does_overwrite_file_if_overwrite_True():
    """ writer = 'w'
    """
    filename='test_writer_overwrite_true.txt'
    writecol(filename=filename, data=[['1', '2', '3', '4'], ['.1', '.2', '.3', '.4']], header=['x', 'y']) 
    with capture_output() as c:
        writecol(filename=filename, data=[['5', '6'], ['.5', '.6']], header=['x', 'y'], writer='w', overwrite=True)
    c()
    out = c.stdout
    assert out.split('\n')[0] == "File '{}' already exists but overwriting/appending with '{}'..."\
        .format(filename, 'w')
    assert readcol(filename=filename) == (['x', 'y'], [['5', '6'], ['.5', '.6']])
    os.remove(filename)

def test_exits_gracefully_if_columns_not_same_len():
    filename='test_write_columns_not_same_len.txt'

    with capture_output() as c:
        writecol(filename=filename, data=[['1', '2', '3'], ['.1', '.2', '.3', '.4']], header=['x', 'y', 'z']) 
    c()
    out = c.stdout
    assert out.split('\n')[1] == "Error: columns not all same length."

def test_exits_gracefully_if_ncols_headerlen_mismatched():
    filename='test_write_mismatched_headerlen.txt'
    # Header length greater than number of columns
    with capture_output() as c:
        writecol(filename=filename, data=[['1', '2', '3', '4'], ['.1', '.2', '.3', '.4']], header=['x', 'y', 'z']) 
    c()
    out = c.stdout
    assert out.split('\n')[1] == "Error: length of header, {}, does not match number of columns, {}."\
        .format(3, 2)

    # Header length less than number of columns
    with capture_output() as c:
        writecol(filename=filename, data=[['1', '2', '3', '4'], ['.1', '.2', '.3', '.4']], header=['x']) 
    c()
    out = c.stdout
    assert out.split('\n')[1] == "Error: length of header, {}, does not match number of columns, {}."\
        .format(1, 2)




