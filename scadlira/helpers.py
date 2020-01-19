import re

NODES_PATTERN = re.compile('\(4/(.*?)[)]')
ELEMENTS_PATTERN = re.compile('\(1/(.*?)[)]')
DOFS_PATTERN = re.compile('\(5/(.*?)[)]')

REPEATER_PATTERN = re.compile('[0-9]+ r [0-9]+ [0-9]+')
INT_PATTERNT = re.compile('[0-9]+')
RANGE_PATTERN = re.compile('[0-9]+\-[0-9]+')

HEADER = """( 0/ 1; scadlira/ 2; 5/
28; 0 1 0  1 0 0  0 0 1; /
33;M 1 CM 100 T 1 C 1 /
39;
1: LOAD 1 ;
 /
)
"""
